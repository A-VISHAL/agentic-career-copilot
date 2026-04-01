# NexusCareer - Complete Implementation Guide

This guide provides step-by-step instructions to recreate the entire NexusCareer application from scratch.

---

## 📋 Table of Contents

1. [Project Initialization](#1-project-initialization)
2. [Backend Implementation](#2-backend-implementation)
3. [Frontend Implementation](#3-frontend-implementation)
4. [Integration & Testing](#4-integration--testing)
5. [Deployment](#5-deployment)

---

## 1. Project Initialization

### 1.1 Create Project Structure

```bash
mkdir nexuscareer
cd nexuscareer
mkdir frontend backend
```

### 1.2 Initialize Git

```bash
git init
echo "node_modules/" > .gitignore
echo "__pycache__/" >> .gitignore
echo ".env" >> .gitignore
echo "uploads/" >> .gitignore
echo ".pytest_cache/" >> .gitignore
echo ".hypothesis/" >> .gitignore
```

---

## 2. Backend Implementation

### 2.1 Setup Python Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2.2 Create requirements.txt

```txt
fastapi==0.115.0
uvicorn[standard]==0.30.6
python-multipart==0.0.9
pydantic==2.9.2
python-dotenv==1.0.1
httpx==0.27.2
openai==1.51.0
spacy==3.7.6
PyMuPDF==1.24.10
python-docx==1.1.2
sentence-transformers==3.1.1
scikit-learn==1.5.2
numpy==1.26.4
shap==0.46.0
dice-ml==0.11
aiofiles==24.1.0
jinja2==3.1.4
redis==5.0.0
pytest==8.3.3
hypothesis==6.115.2
pytest-asyncio==0.24.0
```

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.4 Create Directory Structure

```bash
mkdir -p app/api app/core app/models app/services app/utils tests uploads
touch app/__init__.py
touch app/api/__init__.py app/api/routes.py
touch app/core/__init__.py app/core/config.py
touch app/models/__init__.py app/models/schemas.py
touch app/services/__init__.py
touch app/utils/__init__.py
touch tests/__init__.py
touch main.py
touch .env.example
```

### 2.5 Implement Core Configuration

**File: `backend/app/core/config.py`**

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "NexusCareer API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Explainable AI Career Copilot Backend"
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ADZUNA_APP_ID: str = os.getenv("ADZUNA_APP_ID", "")
    ADZUNA_APP_KEY: str = os.getenv("ADZUNA_APP_KEY", "")
    JSEARCH_API_KEY: str = os.getenv("JSEARCH_API_KEY", "")
    
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    CACHE_TTL_MINUTES: int = int(os.getenv("CACHE_TTL_MINUTES", "15"))
    MAX_JOBS_PER_QUERY: int = int(os.getenv("MAX_JOBS_PER_QUERY", "50"))
    MIN_SKILL_MATCH_RATIO: float = float(os.getenv("MIN_SKILL_MATCH_RATIO", "0.6"))
    MAX_EXPERIENCE_GAP_YEARS: float = float(os.getenv("MAX_EXPERIENCE_GAP_YEARS", "2.0"))
    API_TIMEOUT_SECONDS: int = int(os.getenv("API_TIMEOUT_SECONDS", "5"))

settings = Settings()
```

### 2.6 Implement Data Models

**File: `backend/app/models/schemas.py`**

Create all Pydantic models (see APPLICATION_BLUEPRINT.md for complete schemas):
- ParsedResume
- JobDescription
- MatchResult
- MatchDimension
- CounterfactualSuggestion
- Skill, Experience, Education
- ResumeImprovement
- InterviewQuestion, InterviewFeedback
- CareerRoadmap, RoadmapItem
- JobListing, RawJobListing
- ChatMessage, ChatRequest

### 2.7 Implement Services

#### 2.7.1 Resume Parser

**File: `backend/app/services/parser.py`**

Key functions:
- `extract_text_from_pdf(file_path)` - PyMuPDF extraction
- `extract_text_from_docx(file_path)` - python-docx extraction
- `extract_skills(text)` - Pattern matching for 100+ tech skills
- `extract_experiences(text)` - Section-based parsing
- `extract_education(text)` - Degree extraction
- `extract_projects(text)` - Project detection
- `parse_resume(file_path)` - Main parsing function
- `get_sample_resume()` - Demo data

#### 2.7.2 Semantic Matcher

**File: `backend/app/services/matcher.py`**

Key functions:
- `parse_job_description(jd_text)` - Extract JD structure
- `compute_skill_overlap(resume_skills, jd_skills)` - Skill matching
- `compute_text_similarity(text_a, text_b)` - TF-IDF cosine
- `compute_dimension_scores(resume, jd)` - 5-dimensional scoring
- `generate_counterfactuals(resume, jd, score)` - XAI suggestions
- `compute_role_fit_for_candidate(resume, jd)` - Bilateral scoring
- `match_resume_to_job(resume, jd_text)` - Main matching function

#### 2.7.3 LLM Generator

**File: `backend/app/services/generator.py`**

Key functions:
- `call_llm(system_prompt, user_prompt)` - OpenAI API wrapper
- `rewrite_resume_bullets(experiences, job_context)` - Resume optimization
- `generate_cover_letter(resume_text, jd_text, tone)` - Cover letter
- `generate_interview_questions(jd_text, num)` - Interview prep
- `evaluate_interview_answer(question, answer, context)` - Answer scoring
- `generate_roadmap(resume, jd_text, match_score)` - Career roadmap
- `chat_with_coach(messages, resume_context, job_context)` - AI coach

#### 2.7.4 Job Search

**File: `backend/app/services/job_search.py`**

Key functions:
- `generate_search_query(resume_data)` - Query from resume
- `search_jobs_adzuna(query, location, max_results)` - Adzuna API
- `search_jobs_jsearch(query, location, max_results)` - JSearch API
- `search_jobs_with_fallback(query, location, max_results)` - Resilient search

#### 2.7.5 Additional Services

Create these service files:
- `explainability.py` - SHAP + DiCE analysis
- `recruiter_sim.py` - ATS & recruiter simulation
- `agentic_copilot.py` - LangGraph workflow
- `jobs.py` - Job listing management

### 2.8 Implement API Routes

**File: `backend/app/api/routes.py`**

Implement all endpoints (see APPLICATION_BLUEPRINT.md for complete list):
- Health check
- Resume upload/parsing
- Matching & analysis
- Generation (cover letter, roadmap)
- Interview simulation
- Job search
- Recruiter simulation
- Agentic workflow
- Full pipeline
- Chat

### 2.9 Create Main Application

**File: `backend/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {
        "name": "NexusCareer API",
        "version": settings.VERSION,
        "description": "Explainable AI Career Copilot — HACKHAZARDS '26",
        "docs": "/docs",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### 2.10 Create Environment File

**File: `backend/.env.example`**

```bash
OPENAI_API_KEY=sk-your-key-here
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
JSEARCH_API_KEY=your_api_key
CORS_ORIGINS=http://localhost:5173
UPLOAD_DIR=./uploads
REDIS_URL=redis://localhost:6379
CACHE_TTL_MINUTES=15
MAX_JOBS_PER_QUERY=50
MIN_SKILL_MATCH_RATIO=0.6
MAX_EXPERIENCE_GAP_YEARS=2.0
API_TIMEOUT_SECONDS=5
```

### 2.11 Run Backend

```bash
python main.py
# Server starts on http://localhost:8000
# API docs at http://localhost:8000/docs
```

---

## 3. Frontend Implementation

### 3.1 Initialize React Project

```bash
cd ../frontend
npm create vite@latest . -- --template react
```

### 3.2 Install Dependencies

```bash
npm install axios@1.13.6 framer-motion@12.38.0 lucide-react@0.577.0 react-router-dom@7.13.1 react-dropzone@15.0.0
```

### 3.3 Create Directory Structure

```bash
mkdir -p src/components src/hooks src/utils src/assets public
```

### 3.4 Implement Design System

**File: `frontend/src/index.css`**

Copy the complete CSS from APPLICATION_BLUEPRINT.md, including:
- CSS variables (colors, fonts)
- Reset styles
- Typography
- Component styles (nav, hero, demo, etc.)
- Animations
- Responsive breakpoints

### 3.5 Implement API Layer

**File: `frontend/src/utils/api.js`**

```javascript
const API_BASE = 'http://localhost:8000';

async function apiCall(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...(options.headers || {}),
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `API Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    if (error.message.includes('Failed to fetch')) {
      console.warn('Backend not available, using demo mode');
      return null;
    }
    throw error;
  }
}

// Export all API functions
export async function uploadResume(file) { /* ... */ }
export async function getSampleResume() { /* ... */ }
export async function matchResume(resumeId, jobDescription) { /* ... */ }
// ... (see APPLICATION_BLUEPRINT.md for complete list)
```

### 3.6 Implement Components

Create all components in `frontend/src/components/`:

#### Core Components
1. **Navbar.jsx** - Fixed navigation header
2. **Hero.jsx** - Landing section with animated stats
3. **Marquee.jsx** - Scrolling tech stack
4. **Pipeline.jsx** - 12-step visualization
5. **Demo.jsx** - Interactive resume analyzer
6. **XaiSection.jsx** - Explainability showcase
7. **Features.jsx** - Bento grid features
8. **JobListings.jsx** - Job cards with filters
9. **InterviewSim.jsx** - Chat-based interview
10. **TechStack.jsx** - Technology breakdown
11. **CtaSection.jsx** - Call-to-action
12. **Footer.jsx** - Footer with links

#### Dashboard Components
13. **PipelineDashboard.jsx** - Full pipeline UI
14. **Breadcrumb.jsx** - Navigation breadcrumbs
15. **NavigationButton.jsx** - Accessible nav button
16. **ProgressBar.jsx** - Pipeline progress
17. **StepCard.jsx** - Individual step card

### 3.7 Implement Hooks

**File: `frontend/src/hooks/useKeyboardNavigation.js`**

```javascript
import { useEffect } from 'react'

export function useKeyboardNavigation(onEscape) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && onEscape) {
        onEscape()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [onEscape])
}
```

**File: `frontend/src/hooks/useReducedMotion.js`**

```javascript
import { useEffect, useState } from 'react'

export function useReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false)

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    setPrefersReducedMotion(mediaQuery.matches)

    const handleChange = () => setPrefersReducedMotion(mediaQuery.matches)
    mediaQuery.addEventListener('change', handleChange)
    return () => mediaQuery.removeEventListener('change', handleChange)
  }, [])

  return prefersReducedMotion
}
```

### 3.8 Implement Main App

**File: `frontend/src/App.jsx`**

```javascript
import { useState } from 'react'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Marquee from './components/Marquee'
import Pipeline from './components/Pipeline'
import Demo from './components/Demo'
import XaiSection from './components/XaiSection'
import Features from './components/Features'
import JobListings from './components/JobListings'
import InterviewSim from './components/InterviewSim'
import TechStack from './components/TechStack'
import CtaSection from './components/CtaSection'
import Footer from './components/Footer'
import PipelineDashboard from './components/PipelineDashboard'

function App() {
  const [resumeData, setResumeData] = useState(null)
  const [resumeId, setResumeId] = useState(null)
  const [matchResult, setMatchResult] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [showPipeline, setShowPipeline] = useState(false)

  if (showPipeline) {
    return <PipelineDashboard onNavigateHome={() => setShowPipeline(false)} />
  }

  return (
    <>
      <Navbar onPipelineClick={() => setShowPipeline(true)} />
      <Hero onPipelineClick={() => setShowPipeline(true)} />
      <Marquee />
      <Pipeline />
      <Demo 
        resumeData={resumeData}
        setResumeData={setResumeData}
        resumeId={resumeId}
        setResumeId={setResumeId}
        matchResult={matchResult}
        setMatchResult={setMatchResult}
        jobDescription={jobDescription}
        setJobDescription={setJobDescription}
      />
      <XaiSection matchResult={matchResult} />
      <Features />
      <JobListings />
      <InterviewSim jobDescription={jobDescription} />
      <TechStack />
      <CtaSection />
      <Footer />
    </>
  )
}

export default App
```

### 3.9 Configure Vite

**File: `frontend/vite.config.js`**

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

### 3.10 Update Package.json

**File: `frontend/package.json`**

```json
{
  "name": "nexuscareer-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.13.6",
    "framer-motion": "^12.38.0",
    "lucide-react": "^0.577.0",
    "react": "^19.2.4",
    "react-dom": "^19.2.4",
    "react-dropzone": "^15.0.0",
    "react-router-dom": "^7.13.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^6.0.1",
    "eslint": "^9.39.4",
    "vite": "^8.0.1"
  }
}
```

### 3.11 Run Frontend

```bash
npm run dev
# Opens on http://localhost:5173
```

---

## 4. Integration & Testing

### 4.1 Test Backend Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Get sample resume
curl http://localhost:8000/api/resume/sample

# Test matching
curl -X POST http://localhost:8000/api/match \
  -F "resume_id=sample_demo" \
  -F "job_description=Senior ML Engineer with Python and PyTorch"
```

### 4.2 Test Frontend Integration

1. Open http://localhost:5173
2. Click "Use sample resume"
3. Paste a job description
4. Click "Analyze Match"
5. Verify results display correctly

### 4.3 Test Full Pipeline

1. Click "🚀 View Full Pipeline"
2. Click "Use Sample Data"
3. Click "🚀 Run Full Pipeline"
4. Verify all 12 steps execute
5. Check results display

### 4.4 Run Backend Tests

```bash
cd backend
pytest tests/ -v
```

---

## 5. Deployment

### 5.1 Frontend Deployment (Vercel)

```bash
cd frontend
npm run build
# Deploy dist/ folder to Vercel
```

**Environment Variables:**
- `VITE_API_BASE_URL`: Backend URL

### 5.2 Backend Deployment (Railway)

```bash
cd backend
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile
```

**Environment Variables:**
- All variables from `.env.example`
- Set `CORS_ORIGINS` to frontend URL

### 5.3 Database Setup (Production)

```bash
# PostgreSQL
CREATE DATABASE nexuscareer;

# Redis
# Use managed Redis service (Railway, Upstash)
```

### 5.4 Domain Configuration

- Frontend: `nexuscareer.app`
- Backend: `api.nexuscareer.app`
- Update CORS settings

---

## 6. Verification Checklist

### Backend
- [ ] Server starts without errors
- [ ] `/health` endpoint returns 200
- [ ] `/docs` shows Swagger UI
- [ ] Sample resume loads
- [ ] Matching works
- [ ] All 12 pipeline steps execute

### Frontend
- [ ] Page loads without errors
- [ ] Navigation works
- [ ] Resume upload works
- [ ] Sample data loads
- [ ] Match analysis displays
- [ ] Pipeline dashboard works
- [ ] All animations smooth
- [ ] Responsive on mobile

### Integration
- [ ] Frontend connects to backend
- [ ] API calls succeed
- [ ] Error handling works
- [ ] Demo mode works without API keys
- [ ] Full pipeline completes

---

## 7. Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in main.py
uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
```

**Module not found:**
```bash
pip install -r requirements.txt
```

**CORS errors:**
```python
# Update CORS_ORIGINS in .env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend Issues

**API connection failed:**
```javascript
// Check API_BASE in utils/api.js
const API_BASE = 'http://localhost:8000';
```

**Build errors:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Styling issues:**
```bash
# Ensure index.css is imported in main.jsx
import './index.css'
```

---

## 8. Next Steps

### Enhancements
1. Add user authentication
2. Implement persistent storage
3. Add more job APIs
4. Enhance AI models
5. Add analytics
6. Implement email notifications
7. Add PDF export
8. Create mobile app

### Optimization
1. Add Redis caching
2. Optimize bundle size
3. Implement lazy loading
4. Add service workers
5. Optimize images
6. Add CDN

---

## 9. Resources

### Documentation
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- Vite: https://vitejs.dev/
- OpenAI: https://platform.openai.com/docs

### APIs
- Adzuna: https://developer.adzuna.com/
- JSearch: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch

### Tools
- Postman: API testing
- VS Code: Development
- Git: Version control
- Docker: Containerization

---

**You now have everything needed to recreate NexusCareer from scratch!**

For detailed code examples, refer to APPLICATION_BLUEPRINT.md and the source files.
