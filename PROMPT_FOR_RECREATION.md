# Prompt to Recreate NexusCareer Application

Use this prompt with an AI assistant to recreate the entire NexusCareer application.

---

## 🎯 Project Overview

Create a full-stack AI-powered career copilot application called "NexusCareer" with the following specifications:

### Core Features
1. **Resume Parsing**: Extract structured data from PDF/DOCX resumes
2. **Semantic Matching**: Multi-dimensional job-resume matching with 5 scoring dimensions
3. **Explainable AI**: SHAP feature attribution and counterfactual suggestions
4. **Resume Optimization**: AI-powered bullet rewriting with metrics
5. **Interview Simulation**: Chat-based interview with real-time scoring
6. **Job Search**: Real-time job search with Adzuna API integration
7. **Recruiter Simulation**: ATS screening and human decision logic
8. **Career Roadmap**: Personalized 90-day learning path
9. **Agentic Workflow**: Multi-step autonomous career coaching
10. **Full Pipeline**: 12-step end-to-end processing

---

## 🛠️ Technology Stack

### Backend (Python)
- FastAPI 0.115.0 for REST API
- OpenAI GPT-4o for AI generation
- sentence-transformers for embeddings
- spaCy for NLP
- PyMuPDF for PDF parsing
- SHAP for explainability
- DiCE-ML for counterfactuals
- Pydantic for data validation
- Uvicorn as ASGI server

### Frontend (React)
- React 19.2.4 with Vite 8.0.1
- Vanilla CSS with custom design system
- Axios for HTTP requests
- Framer Motion for animations
- React Router for navigation
- React Dropzone for file uploads

---

## 📁 Project Structure

```
nexuscareer/
├── backend/
│   ├── app/
│   │   ├── api/routes.py          # All REST endpoints
│   │   ├── core/config.py         # Settings & environment
│   │   ├── models/schemas.py      # Pydantic data models
│   │   └── services/
│   │       ├── parser.py          # Resume parsing
│   │       ├── matcher.py         # Semantic matching
│   │       ├── generator.py       # LLM generation
│   │       ├── job_search.py      # Job API integration
│   │       ├── explainability.py  # SHAP + DiCE
│   │       ├── recruiter_sim.py   # ATS simulation
│   │       └── agentic_copilot.py # Workflow engine
│   ├── main.py                    # FastAPI app
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/            # React components
    │   │   ├── Hero.jsx
    │   │   ├── Demo.jsx
    │   │   ├── PipelineDashboard.jsx
    │   │   └── ... (12 more)
    │   ├── utils/api.js           # API client
    │   ├── App.jsx                # Main app
    │   └── index.css              # Design system
    └── package.json
```

---

## 🎨 Design System

### Color Palette
```css
--bg0: #03050A      /* Darkest background */
--bg1: #070B14
--bg2: #0B1120
--bg3: #0F182C
--c1: #00E5B4       /* Primary teal */
--c2: #FF5C6B       /* Error red */
--c3: #6B6BFF       /* Purple */
--c4: #FFB547       /* Orange */
--text: #EDF2FF
--muted: #4A5878
```

### Typography
- Display: Cabinet Grotesk (800 weight)
- Serif: Instrument Serif (italic)
- Mono: Geist Mono

### UI Patterns
- Glassmorphism cards with backdrop blur
- Animated score rings (SVG)
- Gradient overlays
- Smooth transitions (0.2s ease)
- Noise texture overlay

---

## 📊 Data Models (Pydantic)

### Core Models
```python
class Skill(BaseModel):
    name: str
    level: Optional[SkillLevel] = None
    years: Optional[float] = None
    context: Optional[str] = None

class Experience(BaseModel):
    title: str
    company: str
    duration: Optional[str] = None
    description: str
    skills_used: list[str] = []

class ParsedResume(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    skills: list[Skill] = []
    experiences: list[Experience] = []
    education: list[Education] = []
    projects: list[dict] = []
    raw_text: str = ""
    skill_names: list[str] = []

class MatchDimension(BaseModel):
    name: str
    score: float = Field(ge=0, le=100)
    matched_items: list[str] = []
    missing_items: list[str] = []
    shap_value: float = 0.0
    explanation: str = ""

class CounterfactualSuggestion(BaseModel):
    action: str
    current_score: float
    projected_score: float
    impact: str  # "high", "medium", "low"
    description: str

class MatchResult(BaseModel):
    overall_score: float = Field(ge=0, le=100)
    dimensions: list[MatchDimension] = []
    counterfactuals: list[CounterfactualSuggestion] = []
    role_fit_for_candidate: float = Field(ge=0, le=100)
    summary: str = ""
```

---

## 🔄 12-Step Pipeline

### Step 1: User Input
- Upload resume (PDF/DOCX/TXT)
- Paste job description

### Step 2: Resume Parsing
- Extract text using PyMuPDF/python-docx
- Parse skills (100+ tech skills pattern matching)
- Extract experience, education, projects
- Return ParsedResume object

### Step 3: JD Parsing
- Extract title, company, requirements
- Separate required vs preferred skills
- Extract experience requirements
- Return JobDescription object

### Step 4: Semantic Matching
- Compute 5-dimensional scores:
  - Technical Skills (35% weight)
  - Experience Fit (25%)
  - Domain Knowledge (15%)
  - Project Depth (15%)
  - Communication (10%)
- Calculate skill overlap
- Compute text similarity (TF-IDF cosine)
- Return MatchResult with overall score

### Step 5: Explainability
- SHAP feature attribution per dimension
- Positive/negative feature analysis
- Generate counterfactuals: "Add Docker → 74% to 91%"
- Detect bias flags
- Return explainability report

### Step 6: Skill Gap Analysis
- Identify matched vs missing skills
- Prioritize required vs preferred
- Calculate match percentage
- Generate learning recommendations

### Step 7: Resume Optimization
- AI-powered bullet rewriting
- Add metrics and specificity
- Remove generic language
- ATS keyword optimization

### Step 8: Recruiter Simulation
- ATS screening (keyword matching)
- Human recruiter decision logic
- Interview likelihood calculation
- Pass/fail verdict

### Step 9: Application Generation
- Generate tailored cover letter
- Optimize resume for role
- Preserve authentic voice

### Step 10: Agentic Workflow
- Profile analysis
- Action plan creation
- Application tracking
- Interview preparation

### Step 11: Database Storage
- Store parsed resumes (in-memory for demo)
- Cache match results

### Step 12: Visualization
- Interactive dashboard
- Score breakdowns
- Skill charts
- Roadmap timeline

---

## 📡 Key API Endpoints

```python
# Resume
POST /api/resume/upload          # Upload & parse
GET  /api/resume/sample          # Get sample data
POST /api/resume/improve         # Get improvements

# Matching
POST /api/match                  # Match resume to JD
POST /api/explainability         # SHAP + DiCE analysis
POST /api/skill-gap              # Skill gap analysis

# Generation
POST /api/cover-letter           # Generate cover letter
POST /api/roadmap                # Career roadmap

# Interview
POST /api/interview/questions    # Generate questions
POST /api/interview/evaluate     # Evaluate answer

# Jobs
GET  /api/jobs                   # Search jobs
GET  /api/skills/trends          # Skill trends

# Simulation
POST /api/recruiter-simulation   # Recruiter review

# Pipeline
POST /api/pipeline/full          # Run all 12 steps

# Chat
POST /api/chat                   # AI career coach
```

---

## 🎯 Key Algorithms

### Semantic Matching Algorithm
```python
def match_resume_to_job(resume: ParsedResume, jd_text: str) -> MatchResult:
    # 1. Parse JD
    jd = parse_job_description(jd_text)
    
    # 2. Compute dimension scores
    dimensions = compute_dimension_scores(resume, jd)
    
    # 3. Calculate weighted overall score
    weights = [0.35, 0.25, 0.15, 0.15, 0.10]
    overall_score = sum(d.score * w for d, w in zip(dimensions, weights))
    
    # 4. Generate counterfactuals
    counterfactuals = generate_counterfactuals(resume, jd, overall_score)
    
    # 5. Bilateral scoring
    role_fit = compute_role_fit_for_candidate(resume, jd)
    
    return MatchResult(
        overall_score=overall_score,
        dimensions=dimensions,
        counterfactuals=counterfactuals,
        role_fit_for_candidate=role_fit,
        summary=generate_summary(overall_score, dimensions)
    )
```

### Counterfactual Generation
```python
def generate_counterfactuals(resume, jd, current_score):
    skill_overlap = compute_skill_overlap(resume.skill_names, jd.required_skills)
    missing = skill_overlap["missing"]
    
    counterfactuals = []
    per_skill_impact = (100 - current_score) * 0.6 / max(len(missing), 1)
    
    for skill in missing[:3]:
        impact = per_skill_impact * 1.5
        projected = min(current_score + impact, 98)
        
        counterfactuals.append(CounterfactualSuggestion(
            action=f"Add {skill}",
            current_score=current_score,
            projected_score=projected,
            impact="high",
            description=f"Adding {skill} would raise score from {current_score}% to {projected}%"
        ))
    
    return counterfactuals
```

---

## 🎨 Key UI Components

### Demo Component (Interactive Analyzer)
```jsx
function Demo() {
  const [resumeData, setResumeData] = useState(null)
  const [matchResult, setMatchResult] = useState(null)
  const [processing, setProcessing] = useState(false)
  
  const handleAnalyze = async () => {
    setProcessing(true)
    const result = await matchResume(resumeId, jobDescription)
    setMatchResult(result)
    setProcessing(false)
  }
  
  return (
    <div className="demo-section">
      <div className="upload-zone">
        {/* File upload */}
      </div>
      <div className="result-panel">
        {/* Match score ring */}
        {/* Dimension bars */}
        {/* Counterfactuals */}
      </div>
    </div>
  )
}
```

### Pipeline Dashboard
```jsx
function PipelineDashboard() {
  const [currentStep, setCurrentStep] = useState(0)
  const [pipelineData, setPipelineData] = useState(null)
  
  const runFullPipeline = async () => {
    for (let i = 1; i <= 12; i++) {
      setCurrentStep(i)
      await new Promise(resolve => setTimeout(resolve, 500))
    }
    
    const data = await fetch('/api/pipeline/full', {
      method: 'POST',
      body: formData
    }).then(r => r.json())
    
    setPipelineData(data)
  }
  
  return (
    <div>
      {/* Step cards */}
      {/* Progress bar */}
      {/* Results */}
    </div>
  )
}
```

---

## 🔐 Environment Variables

```bash
# Backend .env
OPENAI_API_KEY=sk-...
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
CORS_ORIGINS=http://localhost:5173
UPLOAD_DIR=./uploads
```

---

## 🚀 Implementation Steps

1. **Setup Backend**
   - Create FastAPI app with CORS
   - Implement data models (Pydantic)
   - Create parser service (PyMuPDF, spaCy)
   - Create matcher service (embeddings, SHAP)
   - Create generator service (OpenAI)
   - Implement all API routes
   - Add demo mode fallbacks

2. **Setup Frontend**
   - Create React app with Vite
   - Implement design system (CSS)
   - Create API client layer
   - Build core components (Hero, Demo, Pipeline)
   - Build dashboard components
   - Add animations and interactions
   - Implement state management

3. **Integration**
   - Connect frontend to backend
   - Test all API endpoints
   - Verify full pipeline execution
   - Test demo mode

4. **Polish**
   - Add loading states
   - Implement error handling
   - Add accessibility features
   - Optimize performance
   - Test responsive design

---

## 📝 Sample Data

### Sample Resume (for demo)
```python
SAMPLE_RESUME = ParsedResume(
    name="Arjun Mehta",
    email="arjun.mehta@email.com",
    skills=[
        Skill(name="Python", level="expert", years=4),
        Skill(name="PyTorch", level="advanced", years=3),
        Skill(name="FastAPI", level="advanced", years=2),
        # ... 20+ more skills
    ],
    experiences=[
        Experience(
            title="Senior ML Engineer",
            company="TechCorp AI Labs",
            description="Built NLP pipeline processing 2.3M daily events...",
            skills_used=["Python", "PyTorch", "FastAPI"]
        ),
        # ... more experiences
    ],
    # ... education, projects
)
```

### Sample Job Description
```
Senior ML Engineer
3+ years experience required
Required: Python, PyTorch, FastAPI, NLP, Docker, AWS
Preferred: React, PostgreSQL, Kubernetes
```

---

## 🎯 Success Criteria

The application should:
- ✅ Parse resumes from PDF/DOCX
- ✅ Match resumes to jobs with 5-dimensional scoring
- ✅ Generate counterfactual explanations
- ✅ Optimize resume bullets with AI
- ✅ Simulate recruiter decisions
- ✅ Generate career roadmaps
- ✅ Run full 12-step pipeline
- ✅ Work in demo mode without API keys
- ✅ Display beautiful, animated UI
- ✅ Be fully responsive

---

## 📚 Additional Context

### Key Differentiators
1. **Explainability**: Not just "74% match" but "Add Docker → 91%"
2. **Bilateral Scoring**: How good is the role for YOU?
3. **Anti-Generic**: Preserves authentic voice, adds real metrics
4. **Agentic**: Autonomous multi-step workflow
5. **Demo-Resilient**: Works without API keys

### Design Philosophy
- Premium dark theme with glassmorphism
- Smooth animations (but respect prefers-reduced-motion)
- Clear information hierarchy
- Accessible (ARIA labels, keyboard nav)
- Mobile-first responsive

---

**Use this prompt to recreate the entire NexusCareer application from scratch!**

For detailed implementation, refer to:
- APPLICATION_BLUEPRINT.md (complete architecture)
- IMPLEMENTATION_GUIDE.md (step-by-step instructions)
