from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class Skill(BaseModel):
    name: str
    level: Optional[SkillLevel] = None
    years: Optional[float] = None
    context: Optional[str] = None  # where this skill was used


class Experience(BaseModel):
    title: str
    company: str
    duration: Optional[str] = None
    description: str
    skills_used: list[str] = []


class Education(BaseModel):
    degree: str
    institution: str
    year: Optional[str] = None
    field: Optional[str] = None


class ParsedResume(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    skills: list[Skill] = []
    experiences: list[Experience] = []
    education: list[Education] = []
    projects: list[dict] = []
    raw_text: str = ""
    skill_names: list[str] = []  # flat list for quick matching


class JobDescription(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    description: str
    required_skills: list[str] = []
    preferred_skills: list[str] = []
    experience_required: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None


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
    effort: str  # "low", "medium", "high"
    description: str


class MatchResult(BaseModel):
    overall_score: float = Field(ge=0, le=100)
    dimensions: list[MatchDimension] = []
    counterfactuals: list[CounterfactualSuggestion] = []
    bias_flags: list[str] = []
    role_fit_for_candidate: float = Field(ge=0, le=100, default=0)
    summary: str = ""


class ResumeImprovement(BaseModel):
    original: str
    improved: str
    reason: str
    impact_area: str  # "clarity", "specificity", "metrics", "keywords"


class CoverLetterRequest(BaseModel):
    resume_text: str
    job_description: str
    tone: str = "professional"  # professional, confident, friendly


class InterviewQuestion(BaseModel):
    question: str
    category: str  # "technical", "behavioral", "system_design", "culture"
    difficulty: str  # "easy", "medium", "hard"
    key_points: list[str] = []
    sample_answer: Optional[str] = None


class InterviewFeedback(BaseModel):
    score: float = Field(ge=0, le=100)
    technical_depth: float = Field(ge=0, le=100)
    clarity: float = Field(ge=0, le=100)
    feedback: str
    strengths: list[str] = []
    improvements: list[str] = []
    keywords_used: list[str] = []
    keywords_missed: list[str] = []


class RoadmapItem(BaseModel):
    week: str
    title: str
    description: str
    category: str  # "learn", "build", "apply"
    priority: str  # "high", "medium", "low"
    resources: list[str] = []


class CareerRoadmap(BaseModel):
    target_role: str
    current_level: str
    items: list[RoadmapItem] = []
    estimated_readiness_weeks: int = 0


class JobListing(BaseModel):
    id: str
    title: str
    company: str
    location: str
    salary_range: Optional[str] = None
    description: str
    required_skills: list[str] = []
    match_score: Optional[float] = None
    matched_skills: list[str] = []
    missing_skills: list[str] = []
    url: Optional[str] = None
    remote: bool = False
    job_type: str = "full-time"


class ChatMessage(BaseModel):
    role: str  # "user", "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    resume_context: Optional[str] = None
    job_context: Optional[str] = None
    mode: str = "interview"  # "interview", "coach", "general"
