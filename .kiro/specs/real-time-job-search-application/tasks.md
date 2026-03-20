# Implementation Plan: Real-Time Job Search Application

## Overview

This implementation plan breaks down the Real-Time Job Search and Application Module into discrete coding tasks. The module extends the existing Agentic Career Copilot pipeline (steps 13-16) to fetch, filter, rank, and display job listings using external APIs (Adzuna/JSearch) and ML-based semantic ranking with sentence-transformers.

The implementation follows a bottom-up approach: backend services first, then API endpoints, then frontend components, ensuring each layer is functional before building the next.

## Tasks

- [ ] 1. Set up project dependencies and configuration
  - Install sentence-transformers library in backend/requirements.txt
  - Add httpx for async API calls (if not already present)
  - Add Redis client for caching (optional, can use in-memory fallback)
  - Create .env configuration for API keys (ADZUNA_APP_ID, ADZUNA_APP_KEY, JSEARCH_API_KEY)
  - Add configuration constants for cache TTL, timeouts, and thresholds
  - _Requirements: 1.6, 10.5, 10.6, 11.5_

- [ ] 2. Create data models and schemas
  - [ ] 2.1 Add job-related Pydantic models to backend/app/models/schemas.py
    - Create RawJobListing model for external API responses
    - Create JobRecommendation model for processed job data
    - Create JobRecommendationsResponse model for API responses
    - Create JobSearchPreferences model for user preferences
    - Create JobApplicationTracking model for tracking applications
    - _Requirements: 1.3, 1.4, 4.2, 4.3_
  
  - [ ]* 2.2 Write property test for data model validation
    - **Property 3: Job Parsing Completeness**
    - **Validates: Requirements 1.3, 1.4**
    - Test that parsed job objects contain all required fields
    - _Requirements: 1.3, 1.4_

- [ ] 3. Implement Job Search Service
  - [ ] 3.1 Create backend/app/services/job_search.py
    - Implement generate_search_query() to extract top 5 skills and job titles from resume data
    - Exclude generic terms (Microsoft Office, Email, etc.) from queries
    - Format queries according to API requirements
    - _Requirements: 1.1, 8.1, 8.2, 8.3_
  
  - [ ]* 3.2 Write property test for query generation
    - **Property 1: Query Generation Completeness**
    - **Validates: Requirements 1.1, 8.1, 8.2, 8.3**
    - Test that queries include top 5 skills and exclude generic terms
    - _Requirements: 1.1, 8.1, 8.2, 8.3_
  
  - [ ] 3.3 Implement Adzuna API integration
    - Create search_jobs_adzuna() function with 5-second timeout
    - Parse API responses into RawJobListing objects
    - Extract title, company, description, skills, experience, type, apply_link
    - Handle API errors gracefully
    - _Requirements: 1.2, 1.3, 1.4, 1.5, 10.5_
  
  - [ ] 3.4 Implement JSearch API integration (fallback)
    - Create search_jobs_jsearch() function with same interface as Adzuna
    - Parse JSearch responses into standardized format
    - Handle API errors gracefully
    - _Requirements: 1.2, 1.3, 1.4, 10.1_
  
  - [ ] 3.5 Implement fallback mechanism with caching
    - Create search_jobs_with_fallback() that tries Adzuna first, then JSearch
    - Implement 15-minute cache for successful responses
    - Return empty list if both APIs fail (don't crash)
    - Log all API calls and failures
    - _Requirements: 1.5, 10.1, 10.2, 10.5, 10.6_
  
  - [ ]* 3.6 Write property tests for API integration
    - **Property 2: API Invocation**
    - **Property 4: API Error Handling**
    - **Property 20: API Fallback**
    - **Property 22: Request Timeout**
    - **Property 23: Response Caching**
    - **Validates: Requirements 1.2, 1.5, 10.1, 10.2, 10.5, 10.6**
    - _Requirements: 1.2, 1.5, 10.1, 10.2, 10.5, 10.6_
  
  - [ ]* 3.7 Write unit tests for search service
    - Test query generation with sample resume
    - Test empty results handling
    - Test API timeout scenarios
    - Test cache hit/miss behavior
    - _Requirements: 1.1, 1.5, 10.5, 10.6_

- [ ] 4. Checkpoint - Verify search service functionality
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement Job Filter Service
  - [ ] 5.1 Create backend/app/services/job_filter.py
    - Implement filter_by_skills() with 60% minimum match ratio
    - Calculate skill match ratio and track missing skills
    - Implement filter_by_experience() with 2-year max gap
    - Parse experience requirements from job descriptions (handle ranges)
    - Implement filter_by_job_type() for internship/full-time filtering
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_
  
  - [ ] 5.2 Implement comprehensive filtering function
    - Create apply_all_filters() that chains all filter functions
    - Populate missing_skills array for each job
    - Return filtered jobs with annotations
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 9.1, 9.2_
  
  - [ ]* 5.3 Write property tests for filtering logic
    - **Property 5: Skill-Based Filtering**
    - **Property 6: Experience-Based Filtering**
    - **Property 7: Job Type Filtering**
    - **Property 18: Missing Skills Identification**
    - **Validates: Requirements 2.1-2.6, 9.1, 9.2**
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 9.1, 9.2_
  
  - [ ]* 5.4 Write unit tests for filter edge cases
    - Test jobs with no required skills
    - Test experience ranges (e.g., "3-5 years")
    - Test missing skills calculation
    - Test filter combinations
    - _Requirements: 2.4, 2.5, 9.1_

- [ ] 6. Implement Job Ranker Service
  - [ ] 6.1 Create backend/app/services/job_ranker.py
    - Initialize JobRanker class with sentence-transformers model (all-MiniLM-L6-v2)
    - Implement compute_similarity() using cosine similarity
    - Encode job descriptions and resume text
    - Return normalized similarity scores
    - _Requirements: 3.1, 3.2, 3.3_
  
  - [ ] 6.2 Implement batch ranking with optimization
    - Create rank_jobs() function that processes all jobs
    - Build resume text from skills, experience, and summary
    - Use batch processing for >20 jobs
    - Normalize scores to 0-100 range
    - Sort jobs by match_score descending
    - Complete within 3 seconds for up to 50 jobs
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 11.2_
  
  - [ ]* 6.3 Write property tests for ranking
    - **Property 8: Match Score Bounds**
    - **Property 9: Ranking Order**
    - **Property 24: Batch Processing Activation**
    - **Validates: Requirements 3.3, 3.4, 11.2**
    - _Requirements: 3.3, 3.4, 11.2_
  
  - [ ]* 6.4 Write unit tests for ranking edge cases
    - Test identical job and resume texts (should be ~100% match)
    - Test completely different texts (should be low match)
    - Test batch processing with 20+ jobs
    - Test performance with 50 jobs
    - _Requirements: 3.3, 3.5, 11.2_

- [ ] 7. Checkpoint - Verify all backend services work together
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Create database schema and migrations
  - [ ] 8.1 Create migration script for job_recommendations table
    - Add columns: id, resume_id, job_id, title, company, location, description, salary_range
    - Add JSONB columns: required_skills, matched_skills, missing_skills
    - Add columns: match_score, apply_link, job_type, remote, source, created_at
    - Add foreign key to resumes table
    - Create indexes on resume_id and match_score
    - _Requirements: 12.6_
  
  - [ ] 8.2 Create migration script for job_applications table
    - Add columns: id, resume_id, job_id, applied_at, apply_link, status
    - Add foreign key to resumes table
    - Create index on resume_id
    - _Requirements: 7.4, 7.5_
  
  - [ ]* 8.3 Write unit tests for database operations
    - Test job recommendation insertion and retrieval
    - Test application tracking insertion
    - Test foreign key constraints
    - _Requirements: 12.6_

- [ ] 9. Implement Job Recommendations API endpoint
  - [ ] 9.1 Add /api/jobs/recommendations route to backend/app/api/routes.py
    - Create GET endpoint with query parameters: resume_id, page, per_page, job_type, location
    - Validate resume_id exists (return 404 if not found)
    - Validate pagination parameters (return 400 if invalid)
    - Set per_page max to 50
    - _Requirements: 4.1, 4.6, 4.7_
  
  - [ ] 9.2 Implement endpoint orchestration logic
    - Fetch resume data from database
    - Call job search service with generated query
    - Apply filters using filter service
    - Rank jobs using ranker service
    - Implement pagination logic
    - Store results in job_recommendations table
    - Return JobRecommendationsResponse with jobs array
    - Complete within 8 seconds total
    - _Requirements: 4.2, 4.3, 4.4, 4.7, 11.1, 12.6_
  
  - [ ] 9.3 Implement response caching and error handling
    - Cache responses based on resume_id and timestamp
    - Return empty array with 200 status if no jobs found
    - Return 404 for invalid resume_id
    - Return 503 if both external APIs fail
    - Add comprehensive error logging
    - _Requirements: 4.5, 4.6, 10.2, 11.3_
  
  - [ ]* 9.4 Write property tests for API endpoint
    - **Property 10: API Response Structure**
    - **Property 11: Invalid Resume Handling**
    - **Property 12: Pagination Correctness**
    - **Property 21: Complete API Failure**
    - **Property 25: Result Limiting**
    - **Validates: Requirements 4.2, 4.3, 4.6, 4.7, 10.2, 11.5**
    - _Requirements: 4.2, 4.3, 4.6, 4.7, 10.2, 11.5_
  
  - [ ]* 9.5 Write integration tests for full API flow
    - Test complete flow from resume upload to job recommendations
    - Test pagination with multiple pages
    - Test invalid resume returns 404
    - Test empty results handling
    - _Requirements: 4.1, 4.2, 4.4, 4.5, 4.6_

- [ ] 10. Implement pipeline integration
  - [ ] 10.1 Add pipeline event emission for steps 13-16
    - Emit event for step 13 (job search)
    - Emit event for step 14 (filtering)
    - Emit event for step 15 (ranking)
    - Emit event for step 16 (API response)
    - Follow existing pipeline event patterns
    - _Requirements: 12.4_
  
  - [ ] 10.2 Integrate with existing authentication and authorization
    - Apply same auth patterns as existing endpoints
    - Verify user permissions for resume access
    - _Requirements: 12.2_
  
  - [ ]* 10.3 Write property test for pipeline integration
    - **Property 26: Input Format Compatibility**
    - **Property 27: Pipeline Event Emission**
    - **Validates: Requirements 12.1, 12.4**
    - _Requirements: 12.1, 12.4_

- [ ] 11. Checkpoint - Verify backend is fully functional
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 12. Create frontend components structure
  - [ ] 12.1 Create frontend/src/components/JobRecommendations.jsx
    - Set up component state: jobs, loading, error, filters, page, hasMore, appliedJobs
    - Implement useEffect hook to fetch jobs on mount and filter changes
    - Create fetchJobs() function to call API endpoint
    - Implement error handling with retry functionality
    - Track applied jobs in state and localStorage
    - _Requirements: 5.1, 5.5, 7.4, 7.5, 10.3, 10.4_
  
  - [ ] 12.2 Implement job application tracking
    - Create handleApply() function that opens apply_link in new tab
    - Use window.open with "_blank" target
    - Update appliedJobs state when user clicks apply
    - Persist applied jobs to localStorage
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_
  
  - [ ]* 12.3 Write property tests for JobRecommendations component
    - **Property 16: Apply Button Behavior**
    - **Property 17: Applied Job Indication**
    - **Validates: Requirements 7.2, 7.3, 7.4, 7.5**
    - _Requirements: 7.2, 7.3, 7.4, 7.5_

- [ ] 13. Create JobCard component
  - [ ] 13.1 Create frontend/src/components/JobCard.jsx
    - Display job title, company name, location prominently
    - Display match_score with color-coded badge (high/med/low)
    - Add company logo placeholder or emoji
    - Display salary range and job type metadata
    - Show "Perfect Match" indicator when missing_skills is empty
    - Add fade-in animation for card rendering
    - _Requirements: 5.1, 5.2, 5.6, 9.5_
  
  - [ ] 13.2 Implement Apply Now button
    - Add "Apply Now" button that calls onApply handler
    - Show "✓ Applied" state for previously applied jobs
    - Disable button after application
    - _Requirements: 7.1, 7.2, 7.5_
  
  - [ ]* 13.3 Write property test for JobCard rendering
    - **Property 13: UI Rendering Completeness**
    - **Property 19: Perfect Match Indication**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 9.5**
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 9.5_
  
  - [ ]* 13.4 Write unit tests for JobCard edge cases
    - Test perfect match indicator display
    - Test applied state rendering
    - Test missing skills limit (max 5)
    - _Requirements: 5.2, 7.5, 9.4, 9.5_

- [ ] 14. Create SkillTags component
  - [ ] 14.1 Create frontend/src/components/SkillTags.jsx
    - Display all required_skills as tags
    - Add visual indicators for matched skills (✓) vs missing skills (○)
    - Use distinct styling for matched (green) and missing (gray/red) skills
    - Limit missing skills display to top 5
    - Add tooltips for skill status
    - _Requirements: 5.3, 5.4, 9.3, 9.4_
  
  - [ ]* 14.2 Write unit tests for SkillTags
    - Test matched vs missing skill styling
    - Test 5-skill display limit
    - Test tooltip content
    - _Requirements: 5.4, 9.4_

- [ ] 15. Create JobFilters component
  - [ ] 15.1 Create frontend/src/components/JobFilters.jsx
    - Add job type filter buttons (All Jobs, Full-Time, Internships)
    - Add location input field
    - Highlight active filter button
    - Call onChange handler when filters change
    - Add smooth transition animations for filter changes
    - _Requirements: 6.1, 6.2, 6.5_
  
  - [ ] 15.2 Implement filter state persistence
    - Store filter selections in component state
    - Persist filters during user session
    - Update job count display when filters applied
    - _Requirements: 6.3, 6.4_
  
  - [ ]* 15.3 Write property test for filter functionality
    - **Property 14: Filter Application**
    - **Property 15: Filter Persistence**
    - **Validates: Requirements 6.2, 6.3, 6.4**
    - _Requirements: 6.2, 6.3, 6.4_

- [ ] 16. Create supporting UI components
  - [ ] 16.1 Create LoadingAnimation component
    - Display spinner with accessible loading message
    - Add aria-live="polite" for screen readers
    - Use existing design system styles
    - _Requirements: 5.5_
  
  - [ ] 16.2 Create ErrorMessage component
    - Display user-friendly error messages
    - Add "Retry" button that calls onRetry handler
    - Show different messages for network vs API errors
    - _Requirements: 10.3, 10.4_
  
  - [ ] 16.3 Create JobGrid component
    - Display jobs in responsive grid layout
    - Implement virtual scrolling for >50 jobs
    - Pass appliedJobs and onApply to JobCard components
    - _Requirements: 11.4_

- [ ] 17. Integrate JobRecommendations into PipelineDashboard
  - [ ] 17.1 Update frontend/src/components/PipelineDashboard.jsx
    - Add JobRecommendations section after step 12
    - Wrap in ResultCard with title "Steps 13-16: Job Recommendations" and icon "💼"
    - Pass resumeId and onNavigateHome props
    - Update step definitions to include steps 13-16
    - _Requirements: 12.3, 12.5_
  
  - [ ] 17.2 Update pipeline state management
    - Add job recommendations state to pipeline context
    - Handle navigation between pipeline steps
    - _Requirements: 12.3_
  
  - [ ]* 17.3 Write integration tests for dashboard integration
    - Test JobRecommendations renders in dashboard
    - Test navigation between steps
    - Test state persistence
    - _Requirements: 12.3, 12.5_

- [ ] 18. Add styling and design system integration
  - [ ] 18.1 Create CSS for job components
    - Style JobCard with existing design system patterns
    - Add responsive breakpoints for mobile/tablet/desktop
    - Implement fade-in animations for cards
    - Style filter buttons and controls
    - Add color-coded match score badges
    - Style skill tags with matched/missing indicators
    - _Requirements: 5.6, 6.5, 12.5_
  
  - [ ] 18.2 Ensure accessibility compliance
    - Add proper ARIA labels to all interactive elements
    - Ensure keyboard navigation works for all controls
    - Verify color contrast meets WCAG AA standards
    - Test with screen readers
    - Add focus indicators for keyboard users
    - _Requirements: 5.5, 10.3_

- [ ] 19. Checkpoint - Verify frontend is fully functional
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 20. Performance optimization
  - [ ] 20.1 Optimize backend performance
    - Profile ranking algorithm with 50 jobs
    - Tune batch processing threshold
    - Optimize cache TTL based on usage patterns
    - Add database query optimization
    - _Requirements: 3.5, 11.1, 11.2, 11.3_
  
  - [ ] 20.2 Optimize frontend performance
    - Implement virtual scrolling for large job lists
    - Add debouncing to filter inputs
    - Optimize re-renders with React.memo
    - Lazy load job cards as user scrolls
    - _Requirements: 11.4_
  
  - [ ]* 20.3 Write performance tests
    - Test API response time with 50 jobs (<8 seconds)
    - Test ranking performance (<3 seconds for 50 jobs)
    - Test UI rendering with 100+ jobs
    - _Requirements: 3.5, 4.4, 11.1_

- [ ] 21. End-to-end testing and validation
  - [ ]* 21.1 Write end-to-end tests
    - Test complete user flow: upload resume → view jobs → apply
    - Test filter interactions and job updates
    - Test pagination and infinite scroll
    - Test error scenarios and recovery
    - _Requirements: All requirements_
  
  - [ ]* 21.2 Perform accessibility audit
    - Run automated accessibility tests with axe-core
    - Test keyboard navigation through all components
    - Test with screen readers (NVDA/JAWS)
    - Verify ARIA labels and roles
    - _Requirements: 5.5, 10.3_

- [ ] 22. Final checkpoint - Complete system verification
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional testing tasks and can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties across all inputs
- Unit tests validate specific examples and edge cases
- The implementation follows a bottom-up approach: services → API → UI
- All components should follow existing design system patterns
- Backend uses Python/FastAPI, frontend uses React
- sentence-transformers model (all-MiniLM-L6-v2) will be downloaded on first use
- External API keys must be configured in .env before testing
- Virtual scrolling is critical for performance with large job lists
- Caching reduces API calls and improves response times significantly
