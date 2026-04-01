"""
Job Search Service

This module handles job search query generation and external API integration
for the Real-Time Job Search and Application Module.

Implements:
- Query generation from resume data (Requirements 1.1, 8.1, 8.2, 8.3)
- External API integration with Adzuna and JSearch
- Fallback mechanism for API resilience
- Response caching for performance
"""

import logging
import httpx
from typing import Optional
from app.models.schemas import ParsedResume, RawJobListing

logger = logging.getLogger(__name__)

# Generic terms to exclude from search queries
GENERIC_TERMS = {
    "microsoft office",
    "ms office",
    "email",
    "communication",
    "teamwork",
    "problem solving",
    "time management",
    "organizational skills",
    "attention to detail",
    "multitasking",
    "interpersonal skills",
    "customer service",
    "phone",
    "computer",
    "internet",
    "typing",
    "data entry",
    "filing",
    "scheduling",
    "calendar management",
}


def generate_search_query(resume_data: ParsedResume) -> str:
    """
    Generate optimized search query from resume analysis.
    
    Implements Requirements 1.1, 8.1, 8.2, 8.3:
    - Extracts top 5 most relevant skills from resume
    - Includes job titles from experience
    - Excludes generic terms (Microsoft Office, Email, etc.)
    - Formats according to API requirements
    
    Args:
        resume_data: Parsed resume with skills and experience
        
    Returns:
        Formatted search query string
        
    Logic:
        1. Extract skills and filter out generic terms
        2. Prioritize skills with higher proficiency levels
        3. Extract job titles from experience
        4. Combine top 5 skills with job titles
        5. Format as space-separated query string
    """
    logger.info("Generating search query from resume data")
    
    # Extract and filter skills
    relevant_skills = []
    
    # Process structured skills with levels
    for skill in resume_data.skills:
        skill_name_lower = skill.name.lower().strip()
        
        # Skip generic terms
        if skill_name_lower in GENERIC_TERMS:
            logger.debug(f"Excluding generic term: {skill.name}")
            continue
        
        # Skip very short or generic-sounding skills
        if len(skill_name_lower) <= 2:
            continue
            
        # Add skill with priority based on level
        priority = 0
        if skill.level:
            level_priority = {
                "expert": 4,
                "advanced": 3,
                "intermediate": 2,
                "beginner": 1
            }
            priority = level_priority.get(skill.level.value, 0)
        
        relevant_skills.append((skill.name, priority))
    
    # Also extract from flat skill_names list if available
    for skill_name in resume_data.skill_names:
        skill_name_lower = skill_name.lower().strip()
        
        if skill_name_lower in GENERIC_TERMS:
            continue
        if len(skill_name_lower) <= 2:
            continue
        
        # Add if not already in list
        if not any(s[0].lower() == skill_name_lower for s in relevant_skills):
            relevant_skills.append((skill_name, 0))
    
    # Sort by priority (higher first) and take top 5
    relevant_skills.sort(key=lambda x: x[1], reverse=True)
    top_skills = [skill[0] for skill in relevant_skills[:5]]
    
    logger.info(f"Selected top {len(top_skills)} skills: {top_skills}")
    
    # Extract job titles from experience
    job_titles = []
    for exp in resume_data.experiences:
        if exp.title:
            title = exp.title.strip()
            # Avoid very generic titles
            if title.lower() not in ["employee", "worker", "staff", "member"]:
                job_titles.append(title)
    
    # Take up to 2 most recent job titles
    recent_titles = job_titles[:2] if job_titles else []
    logger.info(f"Extracted job titles: {recent_titles}")
    
    # Combine skills and titles into query
    query_parts = top_skills + recent_titles
    
    # Format as space-separated string
    query = " ".join(query_parts)
    
    logger.info(f"Generated search query: {query}")
    
    return query


async def search_jobs_adzuna(
    query: str,
    location: str = "",
    max_results: int = 50
) -> list[RawJobListing]:
    """
    Query Adzuna API for job listings.
    
    Args:
        query: Search query string
        location: Geographic location filter
        max_results: Maximum number of results (default 50)
        
    Returns:
        List of raw job listings from API
        
    Raises:
        httpx.HTTPError: If API call fails
        httpx.TimeoutException: If request times out
        
    Implementation:
        - 5-second timeout per request
        - Parse response into standardized format
        - Extract: title, company, description, skills, experience, type, apply_link
    """
    from app.core.config import settings
    
    logger.info(f"Searching Adzuna API with query: {query}, location: {location}")
    
    # Validate API credentials
    if not settings.ADZUNA_APP_ID or not settings.ADZUNA_APP_KEY:
        logger.error("Adzuna API credentials not configured")
        raise ValueError("Adzuna API credentials not configured")
    
    # Adzuna API endpoint (US market)
    # Format: https://api.adzuna.com/v1/api/jobs/{country}/search/{page}
    base_url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
    
    # Build query parameters
    params = {
        "app_id": settings.ADZUNA_APP_ID,
        "app_key": settings.ADZUNA_APP_KEY,
        "results_per_page": min(max_results, settings.MAX_JOBS_PER_QUERY),
        "what": query,
        "content-type": "application/json"
    }
    
    # Add location if provided
    if location:
        params["where"] = location
    
    logger.debug(f"Adzuna API request params: {params}")
    
    try:
        # Make API request with 5-second timeout
        async with httpx.AsyncClient(timeout=settings.API_TIMEOUT_SECONDS) as client:
            response = await client.get(base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Adzuna API returned {data.get('count', 0)} total results")
            
            # Parse results into RawJobListing objects
            raw_jobs = []
            results = data.get("results", [])
            
            for job_data in results:
                try:
                    # Extract job type from title/description
                    job_type = "full-time"  # Default
                    title_lower = job_data.get("title", "").lower()
                    description_lower = job_data.get("description", "").lower()
                    
                    if "intern" in title_lower or "internship" in title_lower:
                        job_type = "internship"
                    elif "intern" in description_lower or "internship" in description_lower:
                        job_type = "internship"
                    elif "part-time" in title_lower or "part time" in title_lower:
                        job_type = "part-time"
                    
                    # Build location string
                    location_parts = []
                    if job_data.get("location", {}).get("display_name"):
                        location_parts.append(job_data["location"]["display_name"])
                    elif job_data.get("location", {}).get("area"):
                        location_parts.append(", ".join(job_data["location"]["area"]))
                    location_str = ", ".join(location_parts) if location_parts else "Remote"
                    
                    # Extract salary information
                    salary_min = job_data.get("salary_min")
                    salary_max = job_data.get("salary_max")
                    
                    # Create RawJobListing object
                    raw_job = RawJobListing(
                        external_id=job_data.get("id", ""),
                        title=job_data.get("title", "Unknown Title"),
                        company=job_data.get("company", {}).get("display_name", "Unknown Company"),
                        location=location_str,
                        description=job_data.get("description", ""),
                        salary_min=salary_min,
                        salary_max=salary_max,
                        apply_url=job_data.get("redirect_url", ""),
                        job_type=job_type,
                        posted_date=job_data.get("created", None),
                        source="adzuna"
                    )
                    
                    raw_jobs.append(raw_job)
                    logger.debug(f"Parsed job: {raw_job.title} at {raw_job.company}")
                    
                except Exception as e:
                    logger.warning(f"Failed to parse job listing: {e}")
                    continue
            
            logger.info(f"Successfully parsed {len(raw_jobs)} jobs from Adzuna")
            return raw_jobs
            
    except httpx.TimeoutException as e:
        logger.error(f"Adzuna API request timed out after {settings.API_TIMEOUT_SECONDS} seconds")
        raise
    except httpx.HTTPError as e:
        logger.error(f"Adzuna API HTTP error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error calling Adzuna API: {type(e).__name__}: {e}")
        raise


async def search_jobs_jsearch(
    query: str,
    location: str = "",
    max_results: int = 50
) -> list[RawJobListing]:
    """
    Query JSearch API for job listings (fallback).
    
    Args:
        query: Search query string
        location: Geographic location filter
        max_results: Maximum number of results (default 50)
        
    Returns:
        List of raw job listings from API
        
    Raises:
        httpx.HTTPError: If API call fails
        httpx.TimeoutException: If request times out
    """
    logger.info(f"Searching JSearch API with query: {query}, location: {location}")
    
    # TODO: Implement JSearch API integration
    # This is a placeholder that will be implemented in a future task
    raise NotImplementedError("JSearch API integration not yet implemented")


async def search_jobs_with_fallback(
    query: str,
    location: str = "",
    max_results: int = 50
) -> list[RawJobListing]:
    """
    Search with automatic fallback mechanism.
    
    Implements Requirements 1.2, 1.5, 10.1, 10.2:
    - Tries Adzuna API first
    - Falls back to JSearch API if Adzuna fails
    - Returns empty list if both fail
    - Logs all errors for monitoring
    
    Args:
        query: Search query string
        location: Geographic location filter
        max_results: Maximum number of results (default 50)
        
    Returns:
        List of raw job listings, or empty list if all APIs fail
        
    Logic:
        1. Try Adzuna API
        2. If fails, try JSearch API
        3. If both fail, return empty list and log error
        4. Check cache before making API calls (future enhancement)
        5. Cache successful responses for 15 minutes (future enhancement)
    """
    logger.info(f"Starting job search with fallback for query: {query}")
    
    # Try primary API (Adzuna)
    try:
        results = await search_jobs_adzuna(query, location, max_results)
        logger.info(f"Adzuna API returned {len(results)} results")
        return results
    except (httpx.TimeoutException, httpx.HTTPError, NotImplementedError) as e:
        logger.warning(f"Adzuna API failed: {type(e).__name__}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error with Adzuna API: {type(e).__name__}: {e}")
    
    # Try fallback API (JSearch)
    try:
        results = await search_jobs_jsearch(query, location, max_results)
        logger.info(f"JSearch API (fallback) returned {len(results)} results")
        return results
    except (httpx.TimeoutException, httpx.HTTPError, NotImplementedError) as e:
        logger.warning(f"JSearch API failed: {type(e).__name__}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error with JSearch API: {type(e).__name__}: {e}")
    
    # Both APIs failed
    logger.error("Both Adzuna and JSearch APIs failed, returning empty results")
    return []
