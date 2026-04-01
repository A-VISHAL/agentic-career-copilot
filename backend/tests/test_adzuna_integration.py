"""
Unit tests for Adzuna API integration

Tests the search_jobs_adzuna function to ensure it correctly:
- Makes API requests with proper parameters
- Parses responses into RawJobListing objects
- Handles errors gracefully
- Respects timeout settings
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.job_search import search_jobs_adzuna
from app.models.schemas import RawJobListing
import httpx


@pytest.mark.asyncio
async def test_adzuna_api_success():
    """Test successful Adzuna API call and response parsing."""
    
    # Mock API response
    mock_response_data = {
        "count": 2,
        "results": [
            {
                "id": "12345",
                "title": "Senior Python Developer",
                "company": {"display_name": "Tech Corp"},
                "location": {"display_name": "San Francisco, CA"},
                "description": "We are looking for a senior Python developer...",
                "salary_min": 120000,
                "salary_max": 180000,
                "redirect_url": "https://example.com/apply/12345",
                "created": "2024-01-15T10:00:00Z"
            },
            {
                "id": "67890",
                "title": "Machine Learning Intern",
                "company": {"display_name": "AI Startup"},
                "location": {"display_name": "Remote"},
                "description": "Internship opportunity for ML enthusiasts...",
                "salary_min": None,
                "salary_max": None,
                "redirect_url": "https://example.com/apply/67890",
                "created": "2024-01-14T15:30:00Z"
            }
        ]
    }
    
    # Mock httpx client
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    
    with patch('httpx.AsyncClient', return_value=mock_client):
        results = await search_jobs_adzuna("Python developer", location="San Francisco")
    
    # Verify results
    assert len(results) == 2
    assert all(isinstance(job, RawJobListing) for job in results)
    
    # Check first job
    assert results[0].external_id == "12345"
    assert results[0].title == "Senior Python Developer"
    assert results[0].company == "Tech Corp"
    assert results[0].location == "San Francisco, CA"
    assert results[0].salary_min == 120000
    assert results[0].salary_max == 180000
    assert results[0].apply_url == "https://example.com/apply/12345"
    assert results[0].job_type == "full-time"
    assert results[0].source == "adzuna"
    
    # Check second job (internship detection)
    assert results[1].external_id == "67890"
    assert results[1].title == "Machine Learning Intern"
    assert results[1].job_type == "internship"  # Should detect from title
    assert results[1].source == "adzuna"


@pytest.mark.asyncio
async def test_adzuna_api_timeout():
    """Test that Adzuna API respects timeout settings."""
    
    # Mock timeout exception
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=httpx.TimeoutException("Request timed out"))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    
    with patch('httpx.AsyncClient', return_value=mock_client):
        with pytest.raises(httpx.TimeoutException):
            await search_jobs_adzuna("Python developer")


@pytest.mark.asyncio
async def test_adzuna_api_http_error():
    """Test handling of HTTP errors from Adzuna API."""
    
    # Mock HTTP error
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "401 Unauthorized", 
        request=MagicMock(), 
        response=MagicMock()
    )
    
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    
    with patch('httpx.AsyncClient', return_value=mock_client):
        with pytest.raises(httpx.HTTPStatusError):
            await search_jobs_adzuna("Python developer")


@pytest.mark.asyncio
async def test_adzuna_api_missing_credentials():
    """Test that missing API credentials raise an error."""
    
    with patch('app.services.job_search.settings') as mock_settings:
        mock_settings.ADZUNA_APP_ID = ""
        mock_settings.ADZUNA_APP_KEY = ""
        
        with pytest.raises(ValueError, match="Adzuna API credentials not configured"):
            await search_jobs_adzuna("Python developer")


@pytest.mark.asyncio
async def test_adzuna_api_empty_results():
    """Test handling of empty results from Adzuna API."""
    
    # Mock empty response
    mock_response_data = {
        "count": 0,
        "results": []
    }
    
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    
    with patch('httpx.AsyncClient', return_value=mock_client):
        results = await search_jobs_adzuna("nonexistent_job_xyz")
    
    assert len(results) == 0
    assert isinstance(results, list)


@pytest.mark.asyncio
async def test_adzuna_api_job_type_detection():
    """Test job type detection from title and description."""
    
    # Mock response with various job types
    mock_response_data = {
        "count": 3,
        "results": [
            {
                "id": "1",
                "title": "Software Engineering Internship",
                "company": {"display_name": "Company A"},
                "location": {"display_name": "New York, NY"},
                "description": "Great internship opportunity",
                "redirect_url": "https://example.com/1",
                "created": "2024-01-15T10:00:00Z"
            },
            {
                "id": "2",
                "title": "Part-Time Developer",
                "company": {"display_name": "Company B"},
                "location": {"display_name": "Boston, MA"},
                "description": "Part-time position available",
                "redirect_url": "https://example.com/2",
                "created": "2024-01-15T10:00:00Z"
            },
            {
                "id": "3",
                "title": "Full Stack Developer",
                "company": {"display_name": "Company C"},
                "location": {"display_name": "Seattle, WA"},
                "description": "Looking for an intern to join our team",
                "redirect_url": "https://example.com/3",
                "created": "2024-01-15T10:00:00Z"
            }
        ]
    }
    
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    
    with patch('httpx.AsyncClient', return_value=mock_client):
        results = await search_jobs_adzuna("developer")
    
    # Check job type detection
    assert results[0].job_type == "internship"  # Detected from title
    assert results[1].job_type == "part-time"   # Detected from title
    assert results[2].job_type == "internship"  # Detected from description


@pytest.mark.asyncio
async def test_adzuna_api_malformed_job_skipped():
    """Test that malformed job listings are skipped gracefully."""
    
    # Mock response with one valid and one malformed job
    mock_response_data = {
        "count": 2,
        "results": [
            {
                "id": "12345",
                "title": "Valid Job",
                "company": {"display_name": "Valid Company"},
                "location": {"display_name": "Valid Location"},
                "description": "Valid description",
                "redirect_url": "https://example.com/valid",
                "created": "2024-01-15T10:00:00Z"
            },
            {
                # Malformed job - missing required fields
                "id": "67890"
                # Missing title, company, etc.
            }
        ]
    }
    
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    
    with patch('httpx.AsyncClient', return_value=mock_client):
        results = await search_jobs_adzuna("developer")
    
    # Should only return the valid job
    assert len(results) == 1
    assert results[0].external_id == "12345"
