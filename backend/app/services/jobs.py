"""
Job Search Service
Integrates with job APIs (Adzuna) and provides sample listings for demo.
"""

import httpx
from typing import Optional
from ..models.schemas import JobListing
from ..core.config import settings


# ─── SAMPLE JOB LISTINGS FOR DEMO ───

SAMPLE_JOBS = [
    JobListing(
        id="job_1",
        title="Senior ML Engineer",
        company="Anthropic",
        location="San Francisco, CA",
        salary_range="$180K–$240K",
        description="Join Anthropic's ML team to build safe, beneficial AI systems. Work on RLHF, model training, and inference optimization. Strong Python, PyTorch, and production ML experience required.",
        required_skills=["Python", "PyTorch", "FastAPI", "Docker", "RLHF"],
        match_score=91,
        matched_skills=["Python", "PyTorch", "FastAPI", "RLHF"],
        missing_skills=["Docker"],
        url="https://anthropic.com/careers",
        remote=True,
        job_type="full-time"
    ),
    JobListing(
        id="job_2",
        title="AI Research Engineer",
        company="DeepMind",
        location="London, UK",
        salary_range="£120K–£160K",
        description="Research and implement state-of-the-art AI models. Focus on NLP, reinforcement learning, and scalable training infrastructure. Experience with JAX and TPUs preferred.",
        required_skills=["Python", "JAX", "NLP", "Research", "TPU/XLA"],
        match_score=87,
        matched_skills=["Python", "JAX", "NLP", "Research"],
        missing_skills=["TPU/XLA"],
        url="https://deepmind.com/careers",
        remote=False,
        job_type="full-time"
    ),
    JobListing(
        id="job_3",
        title="ML Platform Engineer",
        company="Stripe",
        location="Remote",
        salary_range="$150K–$200K",
        description="Build and maintain ML infrastructure at Stripe. Design scalable pipelines using Kubernetes, Airflow, and MLflow. Strong systems engineering and ML operations experience needed.",
        required_skills=["Python", "Kubernetes", "Airflow", "SQL", "MLflow"],
        match_score=74,
        matched_skills=["Python", "SQL", "MLflow"],
        missing_skills=["Kubernetes", "Airflow"],
        url="https://stripe.com/jobs",
        remote=True,
        job_type="full-time"
    ),
    JobListing(
        id="job_4",
        title="NLP Engineer",
        company="Cohere",
        location="Toronto, Canada",
        salary_range="$140K–$190K",
        description="Build next-gen NLP models and API services. Work on text embedding, classification, and generation systems. Experience with transformers, spaCy, and FastAPI.",
        required_skills=["Python", "NLP", "Transformers", "spaCy", "FastAPI"],
        match_score=94,
        matched_skills=["Python", "NLP", "Transformers", "spaCy", "FastAPI"],
        missing_skills=[],
        url="https://cohere.com/careers",
        remote=True,
        job_type="full-time"
    ),
    JobListing(
        id="job_5",
        title="Full Stack AI Developer",
        company="Vercel",
        location="Remote (Global)",
        salary_range="$130K–$180K",
        description="Build AI-powered features for Vercel's platform. Full-stack role combining React, Next.js, and LLM integration. TypeScript expertise and AI application experience required.",
        required_skills=["React", "TypeScript", "Next.js", "Python", "LLM"],
        match_score=62,
        matched_skills=["React", "Python"],
        missing_skills=["TypeScript", "Next.js", "LLM"],
        url="https://vercel.com/careers",
        remote=True,
        job_type="full-time"
    ),
    JobListing(
        id="job_6",
        title="Data Scientist — Fraud Detection",
        company="Revolut",
        location="London / Remote",
        salary_range="£90K–£130K",
        description="Build and deploy fraud detection models at scale. Experience with real-time ML systems, Python, scikit-learn, and SQL required. Financial domain knowledge preferred.",
        required_skills=["Python", "scikit-learn", "SQL", "Machine Learning", "Data Engineering"],
        match_score=85,
        matched_skills=["Python", "scikit-learn", "SQL", "Machine Learning"],
        missing_skills=["Data Engineering"],
        url="https://revolut.com/careers",
        remote=True,
        job_type="full-time"
    ),
]


async def search_jobs(
    query: str = "",
    location: str = "",
    category: str = "all",
    page: int = 1,
    per_page: int = 10
) -> list[JobListing]:
    """
    Search for jobs. Uses Adzuna API if credentials available, otherwise returns sample data.
    """
    
    # Try Adzuna API
    if settings.ADZUNA_APP_ID and settings.ADZUNA_APP_KEY:
        try:
            async with httpx.AsyncClient() as client:
                url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}"
                params = {
                    "app_id": settings.ADZUNA_APP_ID,
                    "app_key": settings.ADZUNA_APP_KEY,
                    "results_per_page": per_page,
                    "what": query or "machine learning engineer",
                    "where": location or "",
                    "content-type": "application/json"
                }
                
                response = await client.get(url, params=params, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    jobs = []
                    for result in data.get("results", []):
                        jobs.append(JobListing(
                            id=str(result.get("id", "")),
                            title=result.get("title", "Unknown"),
                            company=result.get("company", {}).get("display_name", "Unknown"),
                            location=result.get("location", {}).get("display_name", ""),
                            salary_range=f"${result.get('salary_min', 'N/A')}–${result.get('salary_max', 'N/A')}" if result.get('salary_min') else None,
                            description=result.get("description", ""),
                            url=result.get("redirect_url", ""),
                            job_type="full-time"
                        ))
                    return jobs
        except Exception as e:
            print(f"Adzuna API error: {e}")
    
    # Filter sample jobs by category
    jobs = SAMPLE_JOBS.copy()
    
    if category == "ml":
        jobs = [j for j in jobs if any(kw in j.title.lower() for kw in ["ml", "machine", "ai", "data", "nlp"])]
    elif category == "backend":
        jobs = [j for j in jobs if any(kw in j.title.lower() for kw in ["backend", "platform", "engineer"])]
    elif category == "fullstack":
        jobs = [j for j in jobs if "full stack" in j.title.lower() or "fullstack" in j.title.lower()]
    elif category == "remote":
        jobs = [j for j in jobs if j.remote]
    
    if query:
        query_lower = query.lower()
        jobs = [j for j in jobs if query_lower in j.title.lower() or query_lower in j.description.lower()]
    
    return jobs


async def get_job_by_id(job_id: str) -> Optional[JobListing]:
    """Get a specific job listing by ID."""
    for job in SAMPLE_JOBS:
        if job.id == job_id:
            return job
    return None


async def get_skill_trends() -> list[dict]:
    """Get trending skills data (mock data for demo)."""
    return [
        {"skill": "Docker", "growth": 34, "direction": "up", "mentions": 12400},
        {"skill": "Kubernetes", "growth": 28, "direction": "up", "mentions": 8900},
        {"skill": "LangChain", "growth": 156, "direction": "up", "mentions": 5200},
        {"skill": "RAG", "growth": 210, "direction": "up", "mentions": 4100},
        {"skill": "PyTorch", "growth": 18, "direction": "up", "mentions": 15600},
        {"skill": "TensorFlow", "growth": -12, "direction": "down", "mentions": 11200},
        {"skill": "FastAPI", "growth": 45, "direction": "up", "mentions": 7800},
        {"skill": "React", "growth": 8, "direction": "stable", "mentions": 28400},
        {"skill": "TypeScript", "growth": 22, "direction": "up", "mentions": 32100},
        {"skill": "Rust", "growth": 67, "direction": "up", "mentions": 3800},
    ]
