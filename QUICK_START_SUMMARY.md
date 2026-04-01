# NexusCareer - Quick Start Summary

## 📋 What is NexusCareer?

An AI-powered career copilot that:
- Analyzes resumes and matches them to jobs
- Explains WHY you match (or don't) using SHAP + DiCE
- Suggests exactly what to add: "Add Docker → 74% to 91%"
- Optimizes your resume with AI
- Simulates recruiter decisions
- Generates personalized career roadmaps

Built for HackHazards '26 AI Track.

---

## 🚀 Run the Application

### Backend (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys (optional - works without)
python main.py
# Opens on http://localhost:8000
```

### Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
# Opens on http://localhost:5173
```

### Access
- Main App: http://localhost:5173
- API Docs: http://localhost:8000/docs
- Pipeline: Click "🚀 View Full Pipeline"

---

## 📁 Key Files

### Backend
- `main.py` - FastAPI entry point
- `app/api/routes.py` - All REST endpoints
- `app/services/matcher.py` - Semantic matching logic
- `app/services/parser.py` - Resume parsing
- `app/services/generator.py` - AI generation
- `app/models/schemas.py` - Data models

### Frontend
- `src/App.jsx` - Main app component
- `src/components/Demo.jsx` - Interactive analyzer
- `src/components/PipelineDashboard.jsx` - Full pipeline UI
- `src/utils/api.js` - API client
- `src/index.css` - Design system

---

## 🎯 Core Features

### 1. Resume Analysis
Upload PDF/DOCX → Extract skills, experience, projects

### 2. Semantic Matching
5-dimensional scoring:
- Technical Skills (35%)
- Experience Fit (25%)
- Domain Knowledge (15%)
- Project Depth (15%)
- Communication (10%)

### 3. Explainability (XAI)
- SHAP feature attribution
- Counterfactuals: "If you add X, score becomes Y"
- Bias detection

### 4. Resume Optimization
AI rewrites bullets:
- Before: "Worked on ML projects"
- After: "Built NLP pipeline processing 2.3M events, reducing alerts by 41%"

### 5. Recruiter Simulation
- ATS screening (keyword matching)
- Human decision logic
- Interview likelihood

### 6. Career Roadmap
Personalized 90-day learning path based on skill gaps

### 7. Full Pipeline
12-step end-to-end processing from upload to visualization

---

## 📡 Key Endpoints

```bash
# Health
GET /health

# Resume
POST /api/resume/upload
GET  /api/resume/sample
POST /api/resume/improve

# Matching
POST /api/match
POST /api/explainability
POST /api/skill-gap

# Generation
POST /api/cover-letter
POST /api/roadmap

# Interview
POST /api/interview/questions
POST /api/interview/evaluate

# Full Pipeline
POST /api/pipeline/full
```

---

## 🎨 Tech Stack

### Backend
- FastAPI (Python)
- OpenAI GPT-4o
- spaCy, PyMuPDF
- SHAP, DiCE-ML
- sentence-transformers

### Frontend
- React 19 + Vite
- Vanilla CSS
- Axios
- Framer Motion

---

## 🔐 Environment Setup

### Required (for full functionality)
```bash
OPENAI_API_KEY=sk-...
ADZUNA_APP_ID=your_id
ADZUNA_APP_KEY=your_key
```

### Optional
```bash
JSEARCH_API_KEY=your_key
REDIS_URL=redis://localhost:6379
```

**Note**: App works in demo mode without API keys!

---

## 📊 Sample Usage

### 1. Quick Demo
1. Open http://localhost:5173
2. Click "Use sample resume"
3. Paste job description (or use pre-filled)
4. Click "Analyze Match"
5. View results in tabs: Match, XAI, Resume, Roadmap

### 2. Full Pipeline
1. Click "🚀 View Full Pipeline"
2. Click "Use Sample Data"
3. Click "🚀 Run Full Pipeline"
4. Watch 12 steps execute
5. View comprehensive results

### 3. Upload Your Resume
1. Click upload zone
2. Select PDF/DOCX file
3. Paste target job description
4. Click "Analyze Match"
5. Get personalized insights

---

## 🎯 Key Algorithms

### Matching Score
```
Overall = (Technical × 0.35) + (Experience × 0.25) + 
          (Domain × 0.15) + (Projects × 0.15) + 
          (Communication × 0.10)
```

### Counterfactual Generation
```
For each missing skill:
  impact = (100 - current_score) × 0.6 / num_missing
  projected = current_score + impact
  return "Add {skill} → {current}% to {projected}%"
```

### Skill Overlap
```
matched = resume_skills ∩ jd_skills
missing = jd_skills - resume_skills
overlap_ratio = |matched| / |jd_skills|
```

---

## 🎨 Design System

### Colors
- Primary: #00E5B4 (Teal)
- Error: #FF5C6B (Red)
- Secondary: #6B6BFF (Purple)
- Accent: #FFB547 (Orange)
- Background: #03050A → #0F182C (Dark gradient)

### Typography
- Display: Cabinet Grotesk (800)
- Serif: Instrument Serif (italic)
- Mono: Geist Mono

### UI Patterns
- Glassmorphism cards
- Animated score rings
- Smooth transitions
- Noise texture overlay

---

## 🔄 12-Step Pipeline

1. **Input** - Upload resume + JD
2. **Parse Resume** - Extract structure
3. **Parse JD** - Extract requirements
4. **Match** - 5-dimensional scoring
5. **Explain** - SHAP + counterfactuals
6. **Skill Gap** - Identify missing skills
7. **Optimize** - Rewrite resume bullets
8. **Simulate** - ATS + recruiter review
9. **Generate** - Cover letter + resume
10. **Agentic** - Workflow automation
11. **Store** - Save results
12. **Visualize** - Interactive dashboard

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt

# Check port
# Change port in main.py if 8000 is taken
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Clear and reinstall
rm -rf node_modules package-lock.json
npm install

# Check port
# Vite uses 5173 by default
```

### CORS errors
```bash
# Update backend .env
CORS_ORIGINS=http://localhost:5173

# Or allow all (dev only)
allow_origins=["*"]
```

### API calls fail
```bash
# Check backend is running
curl http://localhost:8000/health

# Check API_BASE in frontend/src/utils/api.js
const API_BASE = 'http://localhost:8000'
```

---

## 📚 Documentation Files

1. **APPLICATION_BLUEPRINT.md** - Complete architecture
2. **IMPLEMENTATION_GUIDE.md** - Step-by-step build instructions
3. **PROMPT_FOR_RECREATION.md** - AI prompt to recreate app
4. **QUICK_START_SUMMARY.md** - This file

---

## 🎯 Success Checklist

- [ ] Backend starts on port 8000
- [ ] Frontend starts on port 5173
- [ ] Can access /health endpoint
- [ ] Can load sample resume
- [ ] Can analyze match
- [ ] Can view XAI breakdown
- [ ] Can run full pipeline
- [ ] All 12 steps execute
- [ ] Results display correctly
- [ ] UI is responsive

---

## 🚀 Next Steps

### For Development
1. Add user authentication
2. Implement persistent storage (PostgreSQL)
3. Add more job APIs (LinkedIn, Indeed)
4. Enhance AI models
5. Add analytics dashboard

### For Production
1. Deploy backend (Railway, Render)
2. Deploy frontend (Vercel, Netlify)
3. Setup database (PostgreSQL + Redis)
4. Configure domain
5. Add monitoring (Sentry)

---

## 📞 Support

### Issues
- Backend errors: Check logs in terminal
- Frontend errors: Check browser console
- API errors: Check /docs for endpoint details

### Resources
- FastAPI Docs: https://fastapi.tiangolo.com/
- React Docs: https://react.dev/
- OpenAI Docs: https://platform.openai.com/docs

---

## 🎓 Learning Resources

### To Understand the Code
1. Read APPLICATION_BLUEPRINT.md
2. Review backend/app/api/routes.py
3. Study backend/app/services/matcher.py
4. Check frontend/src/components/Demo.jsx
5. Explore frontend/src/index.css

### To Extend the App
1. Add new service in backend/app/services/
2. Add new route in backend/app/api/routes.py
3. Add new component in frontend/src/components/
4. Update API client in frontend/src/utils/api.js

---

## 🏆 Key Achievements

- ✅ Full-stack AI application
- ✅ Explainable AI (SHAP + DiCE)
- ✅ Real-time job matching
- ✅ Resume optimization
- ✅ Interview simulation
- ✅ Career roadmap generation
- ✅ 12-step pipeline
- ✅ Beautiful UI with animations
- ✅ Demo mode (works without API keys)
- ✅ Fully responsive

---

**You're ready to run and explore NexusCareer!**

Start with the Quick Demo, then try the Full Pipeline, then upload your own resume.

For detailed implementation, see the other documentation files.
