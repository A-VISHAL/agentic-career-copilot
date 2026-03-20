"""
NexusCareer API Routes
All REST endpoints for the career copilot application.
"""

import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional

from ..core.config import settings
from ..models.schemas import (
    ChatRequest, CoverLetterRequest, ParsedResume
)
from ..services.parser import parse_resume, get_sample_resume
from ..services.matcher import match_resume_to_job
from ..services.generator import (
    rewrite_resume_bullets, generate_cover_letter,
    generate_interview_questions, evaluate_interview_answer,
    generate_roadmap, chat_with_coach
)
from ..services.jobs import search_jobs, get_job_by_id, get_skill_trends

router = APIRouter()

# In-memory store for parsed resumes (demo purposes)
resume_store: dict[str, ParsedResume] = {}


# ─── HEALTH ───

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "has_openai_key": bool(settings.OPENAI_API_KEY),
        "has_adzuna_key": bool(settings.ADZUNA_APP_ID),
    }


# ─── RESUME PARSING ───

@router.post("/api/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse a resume (PDF or DOCX)."""
    
    # Validate file type
    allowed_extensions = {'.pdf', '.docx', '.doc', '.txt'}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(400, f"Unsupported file type: {ext}. Use PDF, DOCX, or TXT.")
    
    # Save uploaded file
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse resume
        parsed = await parse_resume(file_path)
        
        # Store for later use
        resume_store[file_id] = parsed
        
        return {
            "resume_id": file_id,
            "parsed": parsed.model_dump(),
            "skill_count": len(parsed.skills),
            "experience_count": len(parsed.experiences),
        }
    
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"Error processing resume: {str(e)}")
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/api/resume/sample")
async def get_sample():
    """Get sample resume data for demo purposes."""
    sample = get_sample_resume()
    sample_id = "sample_demo"
    resume_store[sample_id] = sample
    
    return {
        "resume_id": sample_id,
        "parsed": sample.model_dump(),
        "skill_count": len(sample.skills),
        "experience_count": len(sample.experiences),
    }


# ─── MATCHING ───

@router.post("/api/match")
async def match_resume(
    resume_id: str = Form(None),
    job_description: str = Form(...),
    resume_text: str = Form(None)
):
    """Match a resume against a job description with XAI breakdown."""
    
    # Get resume
    resume = None
    if resume_id and resume_id in resume_store:
        resume = resume_store[resume_id]
    elif resume_text:
        # Parse from raw text
        from ..services.parser import extract_skills, extract_experiences, extract_education
        resume = ParsedResume(
            raw_text=resume_text,
            skills=extract_skills(resume_text),
            experiences=extract_experiences(resume_text),
            education=extract_education(resume_text),
            skill_names=[s.name for s in extract_skills(resume_text)]
        )
    else:
        # Use sample for demo
        resume = get_sample_resume()
    
    result = await match_resume_to_job(resume, job_description)
    
    return result.model_dump()


# ─── RESUME IMPROVEMENT ───

@router.post("/api/resume/improve")
async def improve_resume(
    resume_id: str = Form(None),
    job_description: str = Form("")
):
    """Get AI-powered resume improvement suggestions."""
    
    resume = resume_store.get(resume_id, get_sample_resume())
    
    experiences = [{"description": exp.description} for exp in resume.experiences]
    improvements = await rewrite_resume_bullets(experiences, job_description)
    
    return {
        "improvements": [imp.model_dump() for imp in improvements]
    }


# ─── COVER LETTER ───

@router.post("/api/cover-letter")
async def create_cover_letter(request: CoverLetterRequest):
    """Generate a tailored cover letter."""
    
    letter = await generate_cover_letter(
        request.resume_text, 
        request.job_description, 
        request.tone
    )
    
    return {"cover_letter": letter}


# ─── INTERVIEW ───

@router.post("/api/interview/questions")
async def get_interview_questions(
    job_description: str = Form(""),
    num_questions: int = Form(5)
):
    """Generate role-specific interview questions."""
    
    questions = await generate_interview_questions(job_description, num_questions)
    return {"questions": [q.model_dump() for q in questions]}


@router.post("/api/interview/evaluate")
async def evaluate_answer(
    question: str = Form(...),
    answer: str = Form(...),
    job_context: str = Form("")
):
    """Evaluate an interview answer with scoring and feedback."""
    
    feedback = await evaluate_interview_answer(question, answer, job_context)
    return feedback.model_dump()


# ─── ROADMAP ───

@router.post("/api/roadmap")
async def create_roadmap(
    resume_id: str = Form(None),
    job_description: str = Form(...)
):
    """Generate a personalized career roadmap."""
    
    resume = resume_store.get(resume_id, get_sample_resume())
    
    # Get match score first
    match_result = await match_resume_to_job(resume, job_description)
    
    roadmap = await generate_roadmap(resume, job_description, match_result.overall_score)
    
    return roadmap.model_dump()


# ─── JOBS ───

@router.get("/api/jobs")
async def list_jobs(
    query: str = "",
    location: str = "",
    category: str = "all",
    page: int = 1,
    per_page: int = 10
):
    """Search job listings."""
    
    jobs = await search_jobs(query, location, category, page, per_page)
    return {"jobs": [j.model_dump() for j in jobs]}


@router.get("/api/jobs/{job_id}")
async def get_job(job_id: str):
    """Get details for a specific job."""
    
    job = await get_job_by_id(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return job.model_dump()


@router.get("/api/skills/trends")
async def skill_trends():
    """Get trending skills data."""
    
    trends = await get_skill_trends()
    return {"trends": trends}


# ─── CHAT ───

@router.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat with the AI career coach."""
    
    response = await chat_with_coach(
        request.messages,
        request.resume_context or "",
        request.job_context or ""
    )
    
    return {"response": response}


# ─── EXPLAINABILITY (STEP 5) ───

@router.post("/api/explainability")
async def get_explainability(
    resume_id: str = Form(None),
    job_description: str = Form(...)
):
    """Get SHAP + DiCE explainability analysis."""
    from ..services.explainability import generate_explainability_report
    from ..services.matcher import parse_job_description
    
    resume = resume_store.get(resume_id, get_sample_resume())
    jd = parse_job_description(job_description)
    match_result = await match_resume_to_job(resume, job_description)
    
    report = generate_explainability_report(resume, jd, match_result)
    
    return report


# ─── SKILL GAP ANALYSIS (STEP 6) ───

@router.post("/api/skill-gap")
async def analyze_skill_gap(
    resume_id: str = Form(None),
    job_description: str = Form(...)
):
    """Analyze skill gaps and prioritize learning."""
    from ..services.matcher import parse_job_description, compute_skill_overlap
    
    resume = resume_store.get(resume_id, get_sample_resume())
    jd = parse_job_description(job_description)
    
    skill_overlap = compute_skill_overlap(resume.skill_names, jd.required_skills + jd.preferred_skills)
    
    # Prioritize missing skills
    missing_required = [s for s in skill_overlap["missing"] if s in jd.required_skills]
    missing_preferred = [s for s in skill_overlap["missing"] if s in jd.preferred_skills]
    
    return {
        "matched_skills": skill_overlap["matched"],
        "missing_skills": skill_overlap["missing"],
        "missing_required": missing_required,
        "missing_preferred": missing_preferred,
        "priority_skills": missing_required[:5],  # Top 5 to learn
        "skill_match_percentage": round(skill_overlap["overlap_ratio"] * 100, 1),
        "learning_recommendations": [
            {
                "skill": skill,
                "priority": "high" if skill in missing_required else "medium",
                "estimated_time": "2-4 weeks",
                "resources": [f"Official {skill} documentation", "Online courses"]
            }
            for skill in (missing_required + missing_preferred)[:5]
        ]
    }


# ─── RECRUITER SIMULATION (STEP 8) ───

@router.post("/api/recruiter-simulation")
async def simulate_recruiter(
    resume_id: str = Form(None),
    job_description: str = Form(...)
):
    """Simulate recruiter decision-making process."""
    from ..services.recruiter_sim import simulate_recruiter_review, simulate_ats_screening
    from ..services.matcher import parse_job_description
    
    resume = resume_store.get(resume_id, get_sample_resume())
    jd = parse_job_description(job_description)
    match_result = await match_resume_to_job(resume, job_description)
    
    # ATS screening first
    ats_result = simulate_ats_screening(resume, jd)
    
    # Recruiter review (only if passed ATS)
    recruiter_result = simulate_recruiter_review(resume, jd, match_result)
    
    return {
        "ats_screening": ats_result,
        "recruiter_review": recruiter_result,
        "overall_verdict": recruiter_result["decision"],
        "pass_probability": recruiter_result["interview_likelihood"]
    }


# ─── AGENTIC WORKFLOW (STEP 10) ───

@router.post("/api/agent/analyze")
async def agent_analyze(
    resume_id: str = Form(None),
    target_roles: str = Form("ML Engineer,Data Scientist")
):
    """Start agentic workflow - analyze profile."""
    from ..services.agentic_copilot import get_workflow
    
    resume = resume_store.get(resume_id, get_sample_resume())
    workflow = get_workflow()
    
    roles = [r.strip() for r in target_roles.split(",")]
    analysis = workflow.analyze_profile(resume, roles)
    
    return analysis


@router.post("/api/agent/plan")
async def agent_plan(
    resume_id: str = Form(None),
    job_description: str = Form(None)
):
    """Create action plan based on analysis."""
    from ..services.agentic_copilot import get_workflow
    from ..services.matcher import parse_job_description
    
    resume = resume_store.get(resume_id, get_sample_resume())
    workflow = get_workflow()
    
    # First analyze
    analysis = workflow.analyze_profile(resume, ["ML Engineer"])
    
    # Then plan
    jd = parse_job_description(job_description) if job_description else None
    plan = workflow.create_action_plan(analysis, jd)
    
    return plan


@router.get("/api/agent/track")
async def agent_track():
    """Track applications and get reminders."""
    from ..services.agentic_copilot import get_workflow
    
    workflow = get_workflow()
    tracking = workflow.track_applications()
    
    return tracking


@router.get("/api/agent/status")
async def agent_status():
    """Get current workflow status."""
    from ..services.agentic_copilot import get_workflow
    
    workflow = get_workflow()
    status = workflow.get_workflow_status()
    
    return status


@router.post("/api/agent/interview-prep")
async def agent_interview_prep(
    job_title: str = Form("ML Engineer")
):
    """Get interview preparation plan."""
    from ..services.agentic_copilot import get_workflow
    
    workflow = get_workflow()
    prep = workflow.simulate_interview_prep(job_title)
    
    return prep


# ─── FULL PIPELINE (ALL STEPS) ───

@router.post("/api/pipeline/full")
async def run_full_pipeline(
    resume_id: str = Form(None),
    job_description: str = Form(...)
):
    """
    Run the complete pipeline from Step 1 to Step 12.
    Returns all intermediate results.
    """
    from ..services.matcher import parse_job_description
    from ..services.explainability import generate_explainability_report
    from ..services.recruiter_sim import simulate_recruiter_review, simulate_ats_screening
    from ..services.agentic_copilot import get_workflow
    
    # STEP 2: Get parsed resume
    resume = resume_store.get(resume_id, get_sample_resume())
    
    # STEP 3: Parse job description
    jd = parse_job_description(job_description)
    
    # STEP 4: Semantic matching
    match_result = await match_resume_to_job(resume, job_description)
    
    # STEP 5: Explainability (SHAP + DiCE)
    explainability = generate_explainability_report(resume, jd, match_result)
    
    # STEP 6: Skill gap analysis
    from ..services.matcher import compute_skill_overlap
    skill_overlap = compute_skill_overlap(resume.skill_names, jd.required_skills + jd.preferred_skills)
    
    # STEP 7: Resume optimization
    improvements = await rewrite_resume_bullets(
        [{"description": exp.description} for exp in resume.experiences[:3]],
        job_description
    )
    
    # STEP 8: Recruiter simulation
    ats_result = simulate_ats_screening(resume, jd)
    recruiter_result = simulate_recruiter_review(resume, jd, match_result)
    
    # STEP 9: Application generation
    cover_letter = await generate_cover_letter(resume.raw_text, job_description, "professional")
    
    # STEP 10: Agentic workflow
    workflow = get_workflow()
    analysis = workflow.analyze_profile(resume, [jd.title or "Target Role"])
    plan = workflow.create_action_plan(analysis, jd)
    tracking = workflow.track_applications()
    
    return {
        "step_2_resume_parsing": {
            "skills": resume.skill_names,
            "experience_count": len(resume.experiences),
            "projects": [p.get("name", "") for p in resume.projects],
            "education": [e.degree for e in resume.education]
        },
        "step_3_jd_parsing": {
            "title": jd.title,
            "required_skills": jd.required_skills,
            "preferred_skills": jd.preferred_skills,
            "experience_required": jd.experience_required
        },
        "step_4_matching": {
            "overall_score": match_result.overall_score,
            "dimensions": [d.model_dump() for d in match_result.dimensions],
            "summary": match_result.summary
        },
        "step_5_explainability": explainability,
        "step_6_skill_gap": {
            "matched": skill_overlap["matched"],
            "missing": skill_overlap["missing"],
            "priority": [s for s in skill_overlap["missing"] if s in jd.required_skills][:5]
        },
        "step_7_optimization": {
            "improvements": [imp.model_dump() for imp in improvements]
        },
        "step_8_recruiter_sim": {
            "ats": ats_result,
            "recruiter": recruiter_result
        },
        "step_9_application": {
            "cover_letter": cover_letter[:500] + "..." if len(cover_letter) > 500 else cover_letter,
            "optimized_resume": "Generated based on improvements"
        },
        "step_10_agentic": {
            "analysis": analysis,
            "plan": plan,
            "tracking": tracking
        }
    }
