# Requirements Document

## Introduction

This document specifies requirements for the Real-Time Job Search and Application Module, which extends the Agentic Career Copilot application to fetch, filter, rank, and display real-time job listings based on analyzed resume data. The module enables users to discover relevant job opportunities and apply directly through external platforms.

## Glossary

- **Job_Search_Service**: Backend service that queries external job APIs and processes results
- **Job_Filter**: Component that evaluates job listings against candidate qualifications
- **Job_Ranker**: Component that calculates similarity scores between jobs and resume data
- **Job_Recommendations_API**: REST endpoint that returns ranked job listings
- **Job_Card_UI**: Frontend component that displays individual job information
- **Resume_Analysis_Data**: Extracted skills, experience level, and qualifications from pipeline steps 1-12
- **Match_Score**: Numerical value (0-100) representing job-resume similarity
- **Adzuna_API**: External job listing service provider
- **JSearch_API**: Alternative external job listing service provider
- **Apply_Link**: URL to external job application page on platforms like LinkedIn or Naukri
- **Job_Type**: Classification of employment (internship or full-time)
- **Experience_Level**: Required years of experience for a position
- **Required_Skills**: Skills listed as mandatory in job description
- **Candidate_Skills**: Skills extracted from resume during analysis

## Requirements

### Requirement 1: Real-Time Job Search Integration

**User Story:** As a job seeker, I want the system to automatically search for relevant jobs after my resume is analyzed, so that I can discover opportunities matching my qualifications.

#### Acceptance Criteria

1. WHEN resume analysis completes (after pipeline step 12), THE Job_Search_Service SHALL generate a search query from Resume_Analysis_Data
2. THE Job_Search_Service SHALL query at least one external API (Adzuna_API or JSearch_API) with the generated search query
3. WHEN the external API returns results, THE Job_Search_Service SHALL parse job listings into a standardized format
4. THE Job_Search_Service SHALL extract title, company, description, Required_Skills, Experience_Level, Job_Type, and Apply_Link from each listing
5. IF the external API request fails, THEN THE Job_Search_Service SHALL log the error and return an empty result set
6. THE Job_Search_Service SHALL complete the search operation within 5 seconds

### Requirement 2: Job Filtering by Qualifications

**User Story:** As a job seeker, I want jobs filtered based on my qualifications, so that I only see positions I'm eligible for.

#### Acceptance Criteria

1. WHEN job listings are received, THE Job_Filter SHALL compare Required_Skills against Candidate_Skills for each job
2. THE Job_Filter SHALL compare job Experience_Level against candidate experience from Resume_Analysis_Data
3. THE Job_Filter SHALL compare Job_Type against candidate preferences (internship or full-time)
4. THE Job_Filter SHALL retain jobs where the candidate meets at least 60% of Required_Skills
5. THE Job_Filter SHALL exclude jobs where Experience_Level exceeds candidate experience by more than 2 years
6. WHERE the candidate specifies Job_Type preference, THE Job_Filter SHALL exclude jobs of different types

### Requirement 3: Job Ranking by Similarity

**User Story:** As a job seeker, I want jobs ranked by how well they match my profile, so that I can prioritize the best opportunities.

#### Acceptance Criteria

1. WHEN filtered jobs are available, THE Job_Ranker SHALL use sentence-transformers to compute semantic similarity between job descriptions and Resume_Analysis_Data
2. THE Job_Ranker SHALL calculate a Match_Score for each job based on similarity computation
3. THE Job_Ranker SHALL normalize Match_Score to a range of 0 to 100
4. THE Job_Ranker SHALL sort jobs in descending order by Match_Score
5. THE Job_Ranker SHALL complete ranking within 3 seconds for up to 50 jobs

### Requirement 4: Job Recommendations API Endpoint

**User Story:** As a frontend developer, I want a REST API to retrieve ranked job recommendations, so that I can display them to users.

#### Acceptance Criteria

1. THE Job_Recommendations_API SHALL expose a GET endpoint at /jobs/recommendations
2. WHEN the endpoint receives a valid request with resume identifier, THE Job_Recommendations_API SHALL return a JSON array of job objects
3. THE Job_Recommendations_API SHALL include title, company, Match_Score, Apply_Link, Required_Skills, and missing skills in each job object
4. THE Job_Recommendations_API SHALL return results within 8 seconds (includes search, filter, and ranking time)
5. IF no jobs match the criteria, THEN THE Job_Recommendations_API SHALL return an empty array with HTTP 200 status
6. IF the resume identifier is invalid, THEN THE Job_Recommendations_API SHALL return HTTP 404 with an error message
7. THE Job_Recommendations_API SHALL support pagination with query parameters for page number and page size

### Requirement 5: Job Card Display

**User Story:** As a job seeker, I want to see job recommendations in an easy-to-read card format, so that I can quickly evaluate opportunities.

#### Acceptance Criteria

1. WHEN job recommendations are received, THE Job_Card_UI SHALL display each job as a card component
2. THE Job_Card_UI SHALL display job title, company name, and Match_Score prominently on each card
3. THE Job_Card_UI SHALL highlight missing skills that the candidate does not possess
4. THE Job_Card_UI SHALL display Required_Skills with visual indicators for matched and missing skills
5. WHILE job data is loading, THE Job_Card_UI SHALL display a loading animation
6. THE Job_Card_UI SHALL render cards with smooth fade-in animations when data arrives

### Requirement 6: Job Type Filtering UI

**User Story:** As a job seeker, I want to filter displayed jobs by type, so that I can focus on internships or full-time positions.

#### Acceptance Criteria

1. THE Job_Card_UI SHALL provide filter controls for Job_Type selection (internship, full-time, or both)
2. WHEN a user selects a Job_Type filter, THE Job_Card_UI SHALL display only jobs matching the selected type
3. THE Job_Card_UI SHALL update the displayed job count when filters are applied
4. THE Job_Card_UI SHALL persist filter selections during the user session
5. THE Job_Card_UI SHALL apply filter changes with smooth transition animations

### Requirement 7: External Application Redirect

**User Story:** As a job seeker, I want to apply to jobs directly on external platforms, so that I can submit applications without leaving the workflow.

#### Acceptance Criteria

1. THE Job_Card_UI SHALL display an "Apply Now" button on each job card
2. WHEN a user clicks the "Apply Now" button, THE Job_Card_UI SHALL open the Apply_Link in a new browser tab
3. THE Job_Card_UI SHALL use window.open with "_blank" target for external navigation
4. THE Job_Card_UI SHALL track which jobs the user has clicked to apply for
5. WHEN a user returns after applying, THE Job_Card_UI SHALL visually indicate previously clicked jobs

### Requirement 8: Job Search Query Generation

**User Story:** As a system administrator, I want search queries generated intelligently from resume data, so that job results are relevant.

#### Acceptance Criteria

1. WHEN generating a search query, THE Job_Search_Service SHALL include the top 5 most relevant skills from Candidate_Skills
2. THE Job_Search_Service SHALL include job titles or roles mentioned in Resume_Analysis_Data
3. THE Job_Search_Service SHALL exclude generic terms like "Microsoft Office" or "Email" from the query
4. THE Job_Search_Service SHALL format the query according to the selected external API requirements
5. THE Job_Search_Service SHALL log the generated query for debugging purposes

### Requirement 9: Missing Skills Identification

**User Story:** As a job seeker, I want to see which skills I'm missing for each job, so that I can identify areas for improvement.

#### Acceptance Criteria

1. WHEN displaying a job, THE Job_Filter SHALL identify Required_Skills not present in Candidate_Skills
2. THE Job_Recommendations_API SHALL include a "missing_skills" array in each job object
3. THE Job_Card_UI SHALL display missing skills with distinct visual styling (e.g., different color or icon)
4. THE Job_Card_UI SHALL limit the display to the top 5 missing skills per job
5. IF a job has no missing skills, THEN THE Job_Card_UI SHALL display a "Perfect Match" indicator

### Requirement 10: Error Handling and Resilience

**User Story:** As a user, I want the system to handle errors gracefully, so that temporary issues don't break my experience.

#### Acceptance Criteria

1. IF Adzuna_API is unavailable, THEN THE Job_Search_Service SHALL attempt to use JSearch_API as fallback
2. IF both external APIs fail, THEN THE Job_Search_Service SHALL return an error response with HTTP 503 status
3. WHEN an API error occurs, THE Job_Card_UI SHALL display a user-friendly error message
4. THE Job_Card_UI SHALL provide a "Retry" button when job loading fails
5. THE Job_Search_Service SHALL implement request timeout of 5 seconds per external API call
6. THE Job_Search_Service SHALL cache successful API responses for 15 minutes to reduce redundant calls

### Requirement 11: Performance and Scalability

**User Story:** As a system administrator, I want the job search module to perform efficiently, so that users experience minimal wait times.

#### Acceptance Criteria

1. THE Job_Search_Service SHALL process up to 100 job listings within the 8-second total response time
2. THE Job_Ranker SHALL use batch processing for similarity computations when more than 20 jobs are present
3. THE Job_Recommendations_API SHALL implement response caching based on resume identifier and timestamp
4. THE Job_Card_UI SHALL implement virtual scrolling when displaying more than 50 job cards
5. THE Job_Search_Service SHALL limit external API requests to 50 results per query to manage processing time

### Requirement 12: Integration with Existing Pipeline

**User Story:** As a developer, I want the job search module to integrate seamlessly with the existing pipeline, so that it extends current functionality without disruption.

#### Acceptance Criteria

1. THE Job_Search_Service SHALL accept Resume_Analysis_Data in the format produced by pipeline step 12
2. THE Job_Recommendations_API SHALL follow the same authentication and authorization patterns as existing pipeline endpoints
3. THE Job_Card_UI SHALL integrate into the existing PipelineDashboard component as a new section
4. THE Job_Search_Service SHALL emit pipeline events for step 13 (search), step 14 (filter), step 15 (rank), and step 16 (API response)
5. THE Job_Card_UI SHALL use the same design system and component library as existing frontend components
6. THE Job_Search_Service SHALL store job recommendation history in the same database as other pipeline data

