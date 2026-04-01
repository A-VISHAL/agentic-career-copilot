"""
Property-based tests for job parsing and data model validation.

**Validates: Requirements 1.3, 1.4**
"""

from hypothesis import given, strategies as st, settings
import pytest
from app.models.schemas import RawJobListing, JobRecommendation


# Helper strategy for generating valid job types
job_type_strategy = st.sampled_from(["full-time", "internship", "part-time", "contract"])

# Helper strategy for generating valid source names
source_strategy = st.sampled_from(["adzuna", "jsearch"])


# Feature: real-time-job-search-application, Property 3: Job Parsing Completeness
@given(
    external_id=st.text(min_size=1, max_size=100),
    title=st.text(min_size=1, max_size=200),
    company=st.text(min_size=1, max_size=200),
    location=st.text(min_size=1, max_size=200),
    description=st.text(min_size=10, max_size=1000),
    salary_min=st.one_of(st.none(), st.floats(min_value=0, max_value=1000000, allow_nan=False, allow_infinity=False)),
    salary_max=st.one_of(st.none(), st.floats(min_value=0, max_value=1000000, allow_nan=False, allow_infinity=False)),
    apply_url=st.text(min_size=10, max_size=500),
    job_type=job_type_strategy,
    posted_date=st.one_of(st.none(), st.text(min_size=1, max_size=50)),
    source=source_strategy,
)
@settings(max_examples=100)
def test_raw_job_listing_contains_all_required_fields(
    external_id, title, company, location, description,
    salary_min, salary_max, apply_url, job_type, posted_date, source
):
    """
    **Property 3: Job Parsing Completeness**
    
    For any external API response containing job listings, parsing should produce
    job objects where each object contains all required fields: title, company,
    description, required_skills, experience_level, job_type, and apply_link.
    
    **Validates: Requirements 1.3, 1.4**
    
    This test verifies that RawJobListing objects can be created with all required
    fields and that those fields are accessible.
    """
    # Create a RawJobListing object (simulating parsing from external API)
    job = RawJobListing(
        external_id=external_id,
        title=title,
        company=company,
        location=location,
        description=description,
        salary_min=salary_min,
        salary_max=salary_max,
        apply_url=apply_url,
        job_type=job_type,
        posted_date=posted_date,
        source=source,
    )
    
    # Verify all required fields are present and accessible
    assert hasattr(job, "external_id"), "Missing external_id field"
    assert hasattr(job, "title"), "Missing title field"
    assert hasattr(job, "company"), "Missing company field"
    assert hasattr(job, "location"), "Missing location field"
    assert hasattr(job, "description"), "Missing description field"
    assert hasattr(job, "apply_url"), "Missing apply_url field"
    assert hasattr(job, "job_type"), "Missing job_type field"
    assert hasattr(job, "source"), "Missing source field"
    
    # Verify required fields are not None or empty
    assert job.external_id is not None and len(job.external_id) > 0, "external_id cannot be empty"
    assert job.title is not None and len(job.title) > 0, "title cannot be empty"
    assert job.company is not None and len(job.company) > 0, "company cannot be empty"
    assert job.location is not None and len(job.location) > 0, "location cannot be empty"
    assert job.description is not None and len(job.description) > 0, "description cannot be empty"
    assert job.apply_url is not None and len(job.apply_url) > 0, "apply_url cannot be empty"
    assert job.job_type is not None and len(job.job_type) > 0, "job_type cannot be empty"
    assert job.source is not None and len(job.source) > 0, "source cannot be empty"
    
    # Verify field values match input
    assert job.external_id == external_id
    assert job.title == title
    assert job.company == company
    assert job.location == location
    assert job.description == description
    assert job.salary_min == salary_min
    assert job.salary_max == salary_max
    assert job.apply_url == apply_url
    assert job.job_type == job_type
    assert job.posted_date == posted_date
    assert job.source == source


# Feature: real-time-job-search-application, Property 3: Job Parsing Completeness (Extended)
@given(
    job_id=st.text(min_size=1, max_size=100),
    title=st.text(min_size=1, max_size=200),
    company=st.text(min_size=1, max_size=200),
    location=st.text(min_size=1, max_size=200),
    description=st.text(min_size=10, max_size=1000),
    salary_range=st.one_of(st.none(), st.text(min_size=1, max_size=100)),
    required_skills=st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=20),
    matched_skills=st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=20),
    missing_skills=st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=20),
    match_score=st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
    apply_link=st.text(min_size=10, max_size=500),
    job_type=job_type_strategy,
    remote=st.booleans(),
    posted_date=st.one_of(st.none(), st.text(min_size=1, max_size=50)),
    source=source_strategy,
)
@settings(max_examples=100)
def test_job_recommendation_contains_all_required_fields(
    job_id, title, company, location, description, salary_range,
    required_skills, matched_skills, missing_skills, match_score,
    apply_link, job_type, remote, posted_date, source
):
    """
    **Property 3: Job Parsing Completeness (Extended for JobRecommendation)**
    
    For any processed job recommendation, the object should contain all required
    fields including match data: title, company, description, required_skills,
    matched_skills, missing_skills, match_score, job_type, and apply_link.
    
    **Validates: Requirements 1.3, 1.4**
    
    This test verifies that JobRecommendation objects (processed from RawJobListing)
    contain all required fields with proper validation.
    """
    # Create a JobRecommendation object (simulating processed job data)
    job = JobRecommendation(
        id=job_id,
        title=title,
        company=company,
        location=location,
        description=description,
        salary_range=salary_range,
        required_skills=required_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        match_score=match_score,
        apply_link=apply_link,
        job_type=job_type,
        remote=remote,
        posted_date=posted_date,
        source=source,
    )
    
    # Verify all required fields are present and accessible
    assert hasattr(job, "id"), "Missing id field"
    assert hasattr(job, "title"), "Missing title field"
    assert hasattr(job, "company"), "Missing company field"
    assert hasattr(job, "location"), "Missing location field"
    assert hasattr(job, "description"), "Missing description field"
    assert hasattr(job, "required_skills"), "Missing required_skills field"
    assert hasattr(job, "matched_skills"), "Missing matched_skills field"
    assert hasattr(job, "missing_skills"), "Missing missing_skills field"
    assert hasattr(job, "match_score"), "Missing match_score field"
    assert hasattr(job, "apply_link"), "Missing apply_link field"
    assert hasattr(job, "job_type"), "Missing job_type field"
    assert hasattr(job, "remote"), "Missing remote field"
    assert hasattr(job, "source"), "Missing source field"
    
    # Verify required fields are not None or empty (for string fields)
    assert job.id is not None and len(job.id) > 0, "id cannot be empty"
    assert job.title is not None and len(job.title) > 0, "title cannot be empty"
    assert job.company is not None and len(job.company) > 0, "company cannot be empty"
    assert job.location is not None and len(job.location) > 0, "location cannot be empty"
    assert job.description is not None and len(job.description) > 0, "description cannot be empty"
    assert job.apply_link is not None and len(job.apply_link) > 0, "apply_link cannot be empty"
    assert job.job_type is not None and len(job.job_type) > 0, "job_type cannot be empty"
    assert job.source is not None and len(job.source) > 0, "source cannot be empty"
    
    # Verify list fields are not None (can be empty lists)
    assert job.required_skills is not None, "required_skills cannot be None"
    assert job.matched_skills is not None, "matched_skills cannot be None"
    assert job.missing_skills is not None, "missing_skills cannot be None"
    assert isinstance(job.required_skills, list), "required_skills must be a list"
    assert isinstance(job.matched_skills, list), "matched_skills must be a list"
    assert isinstance(job.missing_skills, list), "missing_skills must be a list"
    
    # Verify match_score is within valid range [0, 100]
    assert 0 <= job.match_score <= 100, f"match_score must be in range [0, 100], got {job.match_score}"
    
    # Verify boolean field
    assert isinstance(job.remote, bool), "remote must be a boolean"
    
    # Verify field values match input
    assert job.id == job_id
    assert job.title == title
    assert job.company == company
    assert job.location == location
    assert job.description == description
    assert job.salary_range == salary_range
    assert job.required_skills == required_skills
    assert job.matched_skills == matched_skills
    assert job.missing_skills == missing_skills
    assert job.match_score == match_score
    assert job.apply_link == apply_link
    assert job.job_type == job_type
    assert job.remote == remote
    assert job.posted_date == posted_date
    assert job.source == source


# Feature: real-time-job-search-application, Property 3: Job Parsing Completeness (Validation)
@given(
    match_score=st.floats(allow_nan=False, allow_infinity=False),
)
@settings(max_examples=100)
def test_job_recommendation_validates_match_score_bounds(match_score):
    """
    **Property 3: Job Parsing Completeness (Validation)**
    
    Verify that JobRecommendation properly validates match_score to be within [0, 100].
    Invalid scores should raise a validation error.
    
    **Validates: Requirements 1.3, 1.4**
    """
    from pydantic import ValidationError
    
    # Create minimal valid job data
    job_data = {
        "id": "test_id",
        "title": "Test Job",
        "company": "Test Company",
        "location": "Test Location",
        "description": "Test description for the job posting",
        "match_score": match_score,
        "apply_link": "https://example.com/apply",
        "source": "adzuna",
    }
    
    if 0 <= match_score <= 100:
        # Valid score should create object successfully
        job = JobRecommendation(**job_data)
        assert job.match_score == match_score
    else:
        # Invalid score should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            JobRecommendation(**job_data)
        
        # Verify the error is about match_score
        error_str = str(exc_info.value)
        assert "match_score" in error_str.lower()
