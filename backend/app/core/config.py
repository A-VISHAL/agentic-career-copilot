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
    
    # Job Search Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    CACHE_TTL_MINUTES: int = int(os.getenv("CACHE_TTL_MINUTES", "15"))
    MAX_JOBS_PER_QUERY: int = int(os.getenv("MAX_JOBS_PER_QUERY", "50"))
    MIN_SKILL_MATCH_RATIO: float = float(os.getenv("MIN_SKILL_MATCH_RATIO", "0.6"))
    MAX_EXPERIENCE_GAP_YEARS: float = float(os.getenv("MAX_EXPERIENCE_GAP_YEARS", "2.0"))
    API_TIMEOUT_SECONDS: int = int(os.getenv("API_TIMEOUT_SECONDS", "5"))

settings = Settings()
