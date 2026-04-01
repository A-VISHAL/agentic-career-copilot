# NexusCareer - Complete Application Blueprint

## 🎯 Project Overview

**NexusCareer** is an Explainable AI Career Copilot built for HackHazards '26. It's the first fully explainable, agentic AI career intelligence system that doesn't just match resumes to jobs—it explains exactly why candidates qualify, reveals hidden skill gaps, and autonomously transforms applications.

### Key Differentiators
- **Counterfactual Explainability (XAI)**: Uses SHAP feature attribution and Microsoft DiCE
- **Bias Audit Layer**: EU AI Act compliance using Microsoft Fairlearn
- **Bilateral Matching**: Scores both candidate-for-role and role-for-candidate
- **Skill Velocity Tracker**: Live market data for skill demand
- **Agentic Autopilot**: LangGraph-powered multi-step agent
- **Anti-Generic Resume Engine**: Preserves authentic voice and real metrics

---

## 📁 Project Structure

```
nexuscareer/
├── frontend/                 # React + Vite application
│   ├── src/
│   │   ├── components/       # UI components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Hero.jsx
│   │   │   ├── Marquee.jsx
│   │   │   ├── Pipeline.jsx
│   │   │   ├── Demo.jsx
│   │   │   ├── XaiSection.jsx
│   │   │   ├── Features.jsx
│   │   │   ├── JobListings.jsx
│   │   │   ├── InterviewSim.jsx
│   │   │   ├── TechStack.jsx
│   │   │   ├── CtaSection.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── PipelineDashboard.jsx
│   │   │   ├── Breadcrumb.jsx
│   │   │   ├── NavigationButton.jsx
│   │   │   ├── ProgressBar.jsx
│   │   │   └── StepCard.jsx
│   │   ├── hooks/
│   │   │   ├── useKeyboardNavigation.js
│   │   │   └── useReducedMotion.js
│   │   ├── utils/
│   │   │   └── api.js           # API integration layer
│   │   ├── App.jsx              # Main app component
│   │   ├── App.css
│   │   ├── index.css            # Design system
│   │   └── main.jsx
│   ├── public/
│   │   ├── favicon.svg
│   │   └── icons.svg
│   ├── package.json
│   ├── vite.config.js
│   └── eslint.config.js
│
└── backend/                  # FastAPI Python backend
    ├── app/
    │   ├── api/
    │   │   ├── routes.py         # All REST endpoints
    │   │   └── __init__.py
    │   ├── core/
    │   │   ├── config.py         # Settings & env vars
    │   │   └── __init__.py
    │   ├── models/
    │   │   ├── schemas.py        # Pydantic models
    │   │   └── __init__.py
    │   ├── services/
    │   │   ├── parser.py         # Resume parsing (PyMuPDF, spaCy)
    │   │   ├── matcher.py        # Semantic matching & SHAP
    │   │   ├── generator.py      # LLM orchestration (OpenAI)
    │   │   ├── jobs.py           # Job search (Adzuna API)
    │   │   ├── job_search.py     # Query generation
    │   │   ├── explainability.py # SHAP + DiCE analysis
    │   │   ├── recruiter_sim.py  # ATS & recruiter simulation
    │   │   ├── agentic_copilot.py # LangGraph workflow
    │   │   └── __init__.py
    │   ├── utils/
    │   │   └── __init__.py
    │   └── __init__.py
    ├── tests/
    │   ├── test_adzuna_integration.py
    │   ├── test_job_parsing_properties.py
    │   ├── test_query_generation_properties.py
    │   └── __init__.py
    ├── uploads/                  # Temporary file storage
    ├── main.py                   # FastAPI entry point
    ├── requirements.txt
    └── .env.example
```

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 19.2.4
- **Build Tool**: Vite 8.0.1
- **Styling**: Vanilla CSS with custom design system
- **HTTP Client**: Axios 1.13.6
- **Animation**: Framer Motion 12.38.0
- **Icons**: Lucide React 0.577.0
- **Routing**: React Router DOM 7.13.1
- **File Upload**: React Dropzone 15.0.0

### Backend
- **Framework**: FastAPI 0.115.0
- **Server**: Uvicorn 0.30.6
- **AI/ML**:
  - OpenAI 1.51.0 (GPT-4o)
  - sentence-transformers 3.1.1
  - spaCy 3.7.6
  - scikit-learn 1.5.2
  - SHAP 0.46.0
  - DiCE-ML 0.11
- **Document Processing**:
  - PyMuPDF 1.24.10
  - python-docx 1.1.2
- **Data**: NumPy 1.26.4, Pandas (via scikit-learn)
- **Testing**: pytest 8.3.3, hypothesis 6.115.2
- **Caching**: Redis 5.0.0

---

## 🎨 Design System

### Color Palette
```css
--bg0: #03050A      /* Darkest background */
--bg1: #070B14      /* Dark background */
--bg2: #0B1120      /* Medium background */
--bg3: #0F182C      /* Light background */
--border: rgba(255,255,255,0.07)
--border2: rgba(255,255,255,0.12)
--c1: #00E5B4       /* Primary (Teal) */
--c2: #FF5C6B       /* Error/Warning (Red) */
--c3: #6B6BFF       /* Secondary (Purple) */
--c4: #FFB547       /* Accent (Orange) */
--c5: #33C4FF       /* Info (Blue) */
--text: #EDF2FF     /* Primary text */
--muted: #4A5878    /* Muted text */
--muted2: #7A8CAA   /* Secondary muted */
```

### Typography
- **Display**: Cabinet Grotesk (800 weight)
- **Serif**: Instrument Serif (italic accents)
- **Mono**: Geist Mono (code, metrics)

### Key UI Patterns
- Glassmorphism cards with backdrop blur
- Gradient overlays for depth
- Animated score rings with SVG
- Noise texture overlay for premium feel
- Smooth transitions (0.2s ease)
- Hover states with transform and glow

---

## 🔄 Complete 12-Step Pipeline

### Step 1: User Input Layer
- Upload resume (PDF/DOCX/TXT)
- Paste job description
- Sample data option

### Step 2: Resume Parsing
- Extract text from documents (PyMuPDF, python-docx)
- Parse skills, experience, education, projects
- Regex + pattern matching for skill detection
- Return structured ParsedResume object

### Step 3: Job Description Parsing
- Extract title, company, requirements
- Separate required vs preferred skills
- Extract experience requirements
- Return structured JobDescription object

### Step 4: Semantic Matching
- Multi-dimensional scoring:
  - Technical Skills (35% weight)
  - Experience Fit (25%)
  - Domain Knowledge (15%)
  - Project Depth (15%)
  - Communication (10%)
- Compute skill overlap
- Text similarity (TF-IDF cosine)
- Return MatchResult with overall score

### Step 5: Explainability (SHAP + DiCE)
- SHAP feature attribution per dimension
- Positive/negative feature analysis
- Counterfactual suggestions: "If you add X, score becomes Y"
- Bias detection flags
- Return explainability report

### Step 6: Skill Gap Analysis
- Identify matched vs missing skills
- Prioritize required vs preferred
- Calculate skill match percentage
- Generate learning recommendations
- Return skill gap report

### Step 7: Resume Optimization
- AI-powered bullet rewriting
- Add metrics and specificity
- Remove generic language
- ATS keyword optimization
- Return before/after improvements

### Step 8: Recruiter Simulation
- ATS screening (keyword matching)
- Human recruiter decision logic
- Interview likelihood calculation
- Pass/fail verdict
- Return simulation results

### Step 9: Application Generation
- Generate tailored cover letter
- Optimize resume for role
- Preserve authentic voice
- Return application materials

### Step 10: Agentic Workflow
- Profile analysis
- Action plan creation
- Application tracking
- Interview preparation
- Return workflow status

### Step 11: Database Storage
- Store parsed resumes
- Cache match results
- Track applications
- (In-memory for demo)

### Step 12: Visualization
- Interactive dashboard
- Score breakdowns
- Skill charts
- Roadmap timeline
- Return visual data

---

## 📡 API Endpoints

### Health & Status
```
GET  /health
GET  /
```

### Resume Operations
```
POST /api/resume/upload          # Upload & parse resume
GET  /api/resume/sample          # Get sample resume
POST /api/resume/improve         # Get AI improvements
```

### Matching & Analysis
```
POST /api/match                  # Match resume to JD
POST /api/explainability         # Get SHAP + DiCE analysis
POST /api/skill-gap              # Analyze skill gaps
```

### Generation
```
POST /api/cover-letter           # Generate cover letter
POST /api/roadmap                # Generate career roadmap
```

### Interview
```
POST /api/interview/questions    # Generate questions
POST /api/interview/evaluate     # Evaluate answer
```

### Jobs
```
GET  /api/jobs                   # Search jobs
GET  /api/jobs/{job_id}          # Get job details
GET  /api/skills/trends          # Get skill trends
```

### Simulation
```
POST /api/recruiter-simulation   # Simulate recruiter review
```

### Agentic Workflow
```
POST /api/agent/analyze          # Analyze profile
POST /api/agent/plan             # Create action plan
GET  /api/agent/track            # Track applications
GET  /api/agent/status           # Get workflow status
POST /api/agent/interview-prep   # Interview prep plan
```

### Full Pipeline
```
POST /api/pipeline/full          # Run all 12 steps
```

### Chat
```
POST /api/chat                   # Chat with AI coach
```

---

## 🔐 Environment Variables

### Backend (.env)
```bash
# OpenAI API
OPENAI_API_KEY=sk-...

# Job Search APIs
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
JSEARCH_API_KEY=your_api_key

# Server Config
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
UPLOAD_DIR=./uploads

# Redis (optional)
REDIS_URL=redis://localhost:6379
CACHE_TTL_MINUTES=15

# Job Search Config
MAX_JOBS_PER_QUERY=50
MIN_SKILL_MATCH_RATIO=0.6
MAX_EXPERIENCE_GAP_YEARS=2.0
API_TIMEOUT_SECONDS=5
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Node.js 18+
- Python 3.9+
- (Optional) Redis for caching

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
# Opens on http://localhost:5173
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python main.py
# Opens on http://localhost:8000
```

### Access the Application
1. Open http://localhost:5173
2. Click "🚀 View Full Pipeline" or "Analyze my resume"
3. Upload resume or use sample data
4. Paste job description
5. Click "Run Full Pipeline"

---

## 🎯 Key Features Implementation

### 1. Explainable AI (XAI)
**Location**: `backend/app/services/matcher.py`, `explainability.py`

- SHAP values for each dimension
- Counterfactual generation: "Add Docker → 74% to 91%"
- Feature attribution breakdown
- Bias detection

### 2. Resume Parsing
**Location**: `backend/app/services/parser.py`

- PDF/DOCX text extraction
- Skill pattern matching (100+ tech skills)
- Experience/education extraction
- Project detection
- Fallback to sample data

### 3. Semantic Matching
**Location**: `backend/app/services/matcher.py`

- 5-dimensional scoring
- Weighted aggregation
- Skill overlap computation
- Text similarity (TF-IDF)
- Bilateral scoring (role fit for candidate)

### 4. AI Generation
**Location**: `backend/app/services/generator.py`

- Resume bullet rewriting
- Cover letter generation
- Interview question generation
- Answer evaluation with STAR method
- Career roadmap creation
- Fallback templates when no API key

### 5. Job Search
**Location**: `backend/app/services/job_search.py`, `jobs.py`

- Query generation from resume
- Adzuna API integration
- JSearch API fallback
- Skill-based filtering
- Real-time search

### 6. Recruiter Simulation
**Location**: `backend/app/services/recruiter_sim.py`

- ATS keyword screening
- Human decision logic
- Interview likelihood
- Pass/fail verdict

### 7. Agentic Workflow
**Location**: `backend/app/services/agentic_copilot.py`

- Profile analysis
- Action planning
- Application tracking
- Interview prep
- LangGraph integration

---

## 🎨 UI Components

### Core Components
1. **Navbar**: Fixed header with navigation
2. **Hero**: Landing section with CTA
3. **Marquee**: Scrolling tech stack
4. **Pipeline**: 12-step visualization
5. **Demo**: Interactive resume analyzer
6. **XaiSection**: Explainability showcase
7. **Features**: Bento grid layout
8. **JobListings**: Job cards with match scores
9. **InterviewSim**: Chat-based interview
10. **TechStack**: Technology breakdown
11. **CtaSection**: Final call-to-action
12. **Footer**: Links and credits
13. **PipelineDashboard**: Full pipeline UI

### Reusable Components
- **Breadcrumb**: Navigation breadcrumbs
- **NavigationButton**: Accessible nav button
- **ProgressBar**: Pipeline progress indicator
- **StepCard**: Individual pipeline step

---

## 📊 Data Models (Pydantic Schemas)

### Core Models
- `ParsedResume`: Structured resume data
- `JobDescription`: Parsed job requirements
- `MatchResult`: Match scores + explanations
- `MatchDimension`: Individual dimension score
- `CounterfactualSuggestion`: "What if" scenarios
- `Skill`: Skill with level and context
- `Experience`: Work experience entry
- `Education`: Education entry

### Generation Models
- `ResumeImprovement`: Before/after bullets
- `CoverLetterRequest`: Cover letter input
- `InterviewQuestion`: Question with metadata
- `InterviewFeedback`: Answer evaluation
- `CareerRoadmap`: Personalized roadmap
- `RoadmapItem`: Individual roadmap step

### Job Models
- `JobListing`: Job with match data
- `RawJobListing`: External API data
- `JobRecommendation`: Processed job
- `JobSearchPreferences`: User preferences

### Chat Models
- `ChatMessage`: Chat message
- `ChatRequest`: Chat input

---

## 🧪 Testing

### Test Files
- `test_adzuna_integration.py`: API integration tests
- `test_job_parsing_properties.py`: Property-based tests
- `test_query_generation_properties.py`: Query generation tests

### Run Tests
```bash
cd backend
pytest tests/ -v
```

---

## 🎭 Demo Mode

The application works without API keys by using:
- Pre-computed match results
- Template-based improvements
- Sample resume data
- Mock job listings
- Fallback responses

This ensures the demo is always functional for presentations.

---

## 🔄 State Management

### Frontend State
- `resumeData`: Parsed resume object
- `resumeId`: Backend resume identifier
- `matchResult`: Match analysis results
- `jobDescription`: User-entered JD
- `showPipeline`: Pipeline dashboard toggle
- `processing`: Loading state
- `activeTab`: Current result tab

### Backend State
- `resume_store`: In-memory resume cache (dict)
- Session-based for demo purposes
- Production would use Redis/PostgreSQL

---

## 🎯 Accessibility Features

- Semantic HTML structure
- ARIA labels and roles
- Keyboard navigation support
- Focus management
- Skip to content link
- Reduced motion support
- Color contrast compliance
- Screen reader friendly

---

## 📱 Responsive Design

### Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1023px
- Desktop: 1024px+

### Responsive Patterns
- Grid auto-fit with minmax
- Flexible gap spacing
- Collapsible navigation
- Stacked layouts on mobile
- Touch-friendly targets (44px min)

---

## 🚀 Deployment Considerations

### Frontend
- Build: `npm run build`
- Deploy to: Vercel, Netlify, Railway
- Environment: Set API_BASE URL

### Backend
- ASGI server: Uvicorn
- Deploy to: Railway, Render, AWS
- Environment: Set all .env variables
- CORS: Configure allowed origins

### Database (Production)
- PostgreSQL for resume storage
- Redis for caching
- S3 for file uploads

---

## 📈 Performance Optimizations

- Lazy loading components
- Debounced API calls
- Response caching (15 min TTL)
- Optimized bundle size
- CSS animations with GPU acceleration
- Async/await for all I/O
- Connection pooling for APIs

---

## 🔒 Security Best Practices

- Input validation (Pydantic)
- File type restrictions
- File size limits (5MB)
- CORS configuration
- API key environment variables
- No sensitive data in frontend
- Temporary file cleanup
- SQL injection prevention (ORM)

---

## 📚 Additional Resources

### Documentation
- FastAPI docs: `/docs` (Swagger UI)
- OpenAPI spec: `/openapi.json`
- README.md: Project overview
- ARCHITECTURE.md: Technical details

### External APIs
- Adzuna: https://developer.adzuna.com/
- OpenAI: https://platform.openai.com/docs

---

## 🎓 Learning Path

To understand this codebase:
1. Start with `README.md`
2. Review `backend/main.py` and `frontend/src/App.jsx`
3. Explore `backend/app/api/routes.py` for endpoints
4. Study `backend/app/services/matcher.py` for core logic
5. Check `frontend/src/components/Demo.jsx` for UI flow
6. Review `backend/app/models/schemas.py` for data structures

---

## 🤝 Contributing

This is a hackathon project. To extend:
1. Add new services in `backend/app/services/`
2. Create new components in `frontend/src/components/`
3. Update schemas in `backend/app/models/schemas.py`
4. Add routes in `backend/app/api/routes.py`
5. Write tests in `backend/tests/`

---

## 📝 License

Built for HackHazards '26 - Educational purposes.

---

**Built with ❤️ by the NexusCareer Team**
