"""
Resume Parser Service
Extracts structured data from PDF and DOCX resumes using PyMuPDF and python-docx.
Falls back to regex-based extraction when spaCy models aren't available.
"""

import re
import os
from typing import Optional

from ..models.schemas import ParsedResume, Skill, Experience, Education


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF using PyMuPDF."""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except ImportError:
        return ""
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX using python-docx."""
    try:
        from docx import Document
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return text.strip()
    except ImportError:
        return ""
    except Exception as e:
        print(f"DOCX extraction error: {e}")
        return ""


# Common technical skills for pattern matching
TECH_SKILLS = [
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", "Ruby",
    "React", "Next.js", "Vue", "Angular", "Node.js", "Express", "FastAPI", "Django", "Flask",
    "PyTorch", "TensorFlow", "Keras", "scikit-learn", "Pandas", "NumPy", "Matplotlib",
    "Docker", "Kubernetes", "AWS", "GCP", "Azure", "Terraform", "Jenkins", "CI/CD",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Supabase", "Firebase",
    "Git", "Linux", "REST API", "GraphQL", "gRPC", "WebSocket",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "LLM", "RAG",
    "Data Engineering", "ETL", "Spark", "Airflow", "Kafka", "Hadoop",
    "HTML", "CSS", "Tailwind", "SASS", "Bootstrap",
    "SQL", "NoSQL", "Redis", "RabbitMQ",
    "Agile", "Scrum", "System Design", "Microservices", "API Design",
    "SHAP", "MLflow", "DVC", "Weights & Biases", "Hugging Face",
    "LangChain", "LangGraph", "CrewAI", "OpenAI", "Anthropic", "Claude",
    "spaCy", "NLTK", "Transformers", "BERT", "GPT",
    "JAX", "RLHF", "Fine-tuning", "Prompt Engineering",
    "R", "MATLAB", "Scala", "Kotlin", "Swift",
    "Unity", "Unreal", "Blender",
    "Figma", "Photoshop", "Sketch",
    "Power BI", "Tableau", "Looker",
]

# Normalize skills for case-insensitive matching
SKILL_PATTERNS = {s.lower(): s for s in TECH_SKILLS}


def extract_email(text: str) -> Optional[str]:
    match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    match = re.search(r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]{7,15}', text)
    return match.group(0).strip() if match else None


def extract_name(text: str) -> Optional[str]:
    """Try to extract name from first non-empty lines."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if lines:
        first_line = lines[0]
        # If first line is short and doesn't look like a section header
        if len(first_line) < 60 and not any(kw in first_line.lower() for kw in ['resume', 'cv', 'curriculum', 'objective', 'summary']):
            return first_line
    return None


def extract_skills(text: str) -> list[Skill]:
    """Extract skills from resume text using pattern matching."""
    found_skills = []
    text_lower = text.lower()
    
    for skill_lower, skill_proper in SKILL_PATTERNS.items():
        # Use word boundary matching
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(Skill(
                name=skill_proper,
                context="Found in resume text"
            ))
    
    return found_skills


def extract_experiences(text: str) -> list[Experience]:
    """Extract work experiences using section-based parsing."""
    experiences = []
    
    # Look for experience section
    exp_pattern = r'(?:experience|work\s*history|employment|professional\s*background)[\s:]*\n([\s\S]*?)(?=\n\s*(?:education|skills|projects|certifications|awards|references|$))'
    match = re.search(exp_pattern, text, re.IGNORECASE)
    
    if match:
        exp_text = match.group(1)
        # Split by common patterns (bullet points, dashes, company headers)
        entries = re.split(r'\n(?=[A-Z][a-zA-Z\s]+(?:[-–|,]|\sat\s))', exp_text)
        
        for entry in entries:
            entry = entry.strip()
            if len(entry) > 20:
                lines = entry.split('\n')
                title = lines[0].strip() if lines else "Position"
                company = lines[1].strip() if len(lines) > 1 else "Company"
                desc = '\n'.join(lines[2:]).strip() if len(lines) > 2 else entry
                
                experiences.append(Experience(
                    title=title[:100],
                    company=company[:100],
                    description=desc[:500],
                    skills_used=[]
                ))
    
    # If no structured experience found, create from text blocks
    if not experiences:
        # Look for job-title-like patterns
        job_patterns = re.findall(
            r'((?:Senior\s+|Junior\s+|Lead\s+|Staff\s+)?(?:Software|ML|AI|Data|Full[\s-]?Stack|Backend|Frontend|DevOps|Cloud|Product|Project)\s+(?:Engineer|Developer|Scientist|Analyst|Manager|Architect|Designer))',
            text, re.IGNORECASE
        )
        for title in job_patterns[:5]:
            experiences.append(Experience(
                title=title.strip(),
                company="Extracted from resume",
                description="Role mentioned in resume",
            ))
    
    return experiences[:10]


def extract_education(text: str) -> list[Education]:
    """Extract education entries."""
    education = []
    
    edu_pattern = r'(?:education|academic|qualification|degree)[\s:]*\n([\s\S]*?)(?=\n\s*(?:experience|skills|projects|work|employment|$))'
    match = re.search(edu_pattern, text, re.IGNORECASE)
    
    if match:
        edu_text = match.group(1)
        # Look for degree patterns
        degree_patterns = re.findall(
            r'((?:B\.?S\.?|M\.?S\.?|Ph\.?D\.?|Bachelor|Master|MBA|B\.?Tech|M\.?Tech|B\.?E\.?|M\.?E\.?)[\w\s.,()-]*)',
            edu_text, re.IGNORECASE
        )
        for deg in degree_patterns[:5]:
            education.append(Education(
                degree=deg.strip()[:100],
                institution="Extracted from resume",
            ))
    
    if not education:
        # Try broader search
        degree_mentions = re.findall(
            r'((?:B\.?S\.?|M\.?S\.?|Ph\.?D\.?|Bachelor|Master|MBA|B\.?Tech|M\.?Tech)[\w\s.,()-]{0,80})',
            text, re.IGNORECASE
        )
        for deg in degree_mentions[:3]:
            education.append(Education(
                degree=deg.strip(),
                institution="",
            ))
    
    return education


def extract_projects(text: str) -> list[dict]:
    """Extract project mentions."""
    projects = []
    
    proj_pattern = r'(?:projects?|portfolio)[\s:]*\n([\s\S]*?)(?=\n\s*(?:experience|education|skills|certifications|awards|$))'
    match = re.search(proj_pattern, text, re.IGNORECASE)
    
    if match:
        proj_text = match.group(1)
        entries = re.split(r'\n(?=[A-Z•●\-])', proj_text)
        for entry in entries:
            entry = entry.strip()
            if len(entry) > 15:
                projects.append({
                    "name": entry.split('\n')[0][:100],
                    "description": entry[:300]
                })
    
    return projects[:10]


async def parse_resume(file_path: str) -> ParsedResume:
    """
    Main parsing function. Extracts structured data from a resume file.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.pdf':
        raw_text = extract_text_from_pdf(file_path)
    elif ext in ['.docx', '.doc']:
        raw_text = extract_text_from_docx(file_path)
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            raw_text = f.read()
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    
    if not raw_text:
        raise ValueError("Could not extract text from the file")
    
    # Extract all components
    skills = extract_skills(raw_text)
    experiences = extract_experiences(raw_text)
    education = extract_education(raw_text)
    projects = extract_projects(raw_text)
    
    return ParsedResume(
        name=extract_name(raw_text),
        email=extract_email(raw_text),
        phone=extract_phone(raw_text),
        skills=skills,
        experiences=experiences,
        education=education,
        projects=projects,
        raw_text=raw_text,
        skill_names=[s.name for s in skills]
    )


# ─── SAMPLE DATA FOR DEMO ─── 
SAMPLE_RESUME_TEXT = """
Arjun Mehta
arjun.mehta@email.com | +91-98765-43210

SUMMARY
Machine Learning Engineer with 4 years of experience building production ML systems. 
Skilled in Python, PyTorch, FastAPI, and NLP. Passionate about deploying models at scale.

EXPERIENCE

Senior ML Engineer — TechCorp AI Labs
Jan 2023 – Present
- Built NLP classification pipeline processing 2.3M daily events, reducing false-positive alerts by 41%
- Led 3-person ML team to ship real-time fraud detection model in 6 weeks, blocking $840K in Q1
- Designed REST APIs using FastAPI serving 50K+ predictions/day with <100ms latency
- Implemented A/B testing framework for model comparison across 12 experiments

ML Engineer — DataFlow Inc.
Aug 2020 – Dec 2022
- Developed sentiment analysis model achieving 93% accuracy on customer feedback data
- Built automated data pipeline using Python, Pandas, and scikit-learn
- Created model monitoring dashboard tracking drift, latency, and accuracy metrics
- Collaborated with product team to define ML feature requirements

PROJECTS

Resume Intelligence Engine
Full-stack application using spaCy for NER-based resume parsing. FastAPI backend with React frontend.
GitHub: 200+ stars

Semantic Search Engine
Built sentence-transformer based document search system processing 1M+ documents.
Achieved 94% retrieval accuracy using FAISS indexing.

EDUCATION
B.Tech in Computer Science — IIT Delhi, 2020
GPA: 8.7/10

SKILLS
Python, PyTorch, TensorFlow, scikit-learn, FastAPI, Flask, React, SQL, PostgreSQL, 
MongoDB, Git, Linux, NLP, Computer Vision, Machine Learning, Deep Learning,
spaCy, Hugging Face, Transformers, REST API, Pandas, NumPy
"""


def get_sample_resume() -> ParsedResume:
    """Return a pre-built sample resume for demo purposes."""
    return ParsedResume(
        name="Arjun Mehta",
        email="arjun.mehta@email.com",
        phone="+91-98765-43210",
        summary="Machine Learning Engineer with 4 years of experience building production ML systems.",
        skills=[
            Skill(name="Python", level="expert", years=4, context="Primary language across all projects"),
            Skill(name="PyTorch", level="advanced", years=3, context="Fraud detection, NLP models"),
            Skill(name="FastAPI", level="advanced", years=2, context="Production APIs, 50K+ pred/day"),
            Skill(name="Machine Learning", level="advanced", years=4, context="Classification, NLP, CV"),
            Skill(name="NLP", level="advanced", years=3, context="Sentiment analysis, classification"),
            Skill(name="scikit-learn", level="advanced", years=4),
            Skill(name="React", level="intermediate", years=1),
            Skill(name="SQL", level="intermediate", years=3),
            Skill(name="PostgreSQL", level="intermediate", years=2),
            Skill(name="MongoDB", level="intermediate", years=1),
            Skill(name="Git", level="advanced", years=4),
            Skill(name="spaCy", level="advanced", years=2),
            Skill(name="Hugging Face", level="intermediate", years=1),
            Skill(name="Transformers", level="intermediate", years=2),
            Skill(name="REST API", level="advanced", years=3),
            Skill(name="Pandas", level="advanced", years=4),
            Skill(name="NumPy", level="advanced", years=4),
            Skill(name="TensorFlow", level="intermediate", years=2),
            Skill(name="Deep Learning", level="advanced", years=3),
            Skill(name="Computer Vision", level="intermediate", years=1),
            Skill(name="Linux", level="intermediate", years=3),
            Skill(name="Flask", level="intermediate", years=2),
        ],
        experiences=[
            Experience(
                title="Senior ML Engineer",
                company="TechCorp AI Labs",
                duration="Jan 2023 – Present",
                description="Built NLP classification pipeline processing 2.3M daily events. Led 3-person ML team. Designed FastAPI REST APIs serving 50K+ predictions/day.",
                skills_used=["Python", "PyTorch", "FastAPI", "NLP", "A/B Testing"]
            ),
            Experience(
                title="ML Engineer",
                company="DataFlow Inc.",
                duration="Aug 2020 – Dec 2022",
                description="Developed sentiment analysis model achieving 93% accuracy. Built automated data pipelines. Created model monitoring dashboard.",
                skills_used=["Python", "Pandas", "scikit-learn", "Machine Learning"]
            )
        ],
        education=[
            Education(
                degree="B.Tech in Computer Science",
                institution="IIT Delhi",
                year="2020",
                field="Computer Science"
            )
        ],
        projects=[
            {"name": "Resume Intelligence Engine", "description": "Full-stack application using spaCy for NER-based resume parsing. FastAPI backend with React frontend. 200+ GitHub stars."},
            {"name": "Semantic Search Engine", "description": "Built sentence-transformer based document search system processing 1M+ documents. 94% retrieval accuracy using FAISS indexing."}
        ],
        raw_text=SAMPLE_RESUME_TEXT,
        skill_names=["Python", "PyTorch", "FastAPI", "Machine Learning", "NLP", "scikit-learn",
                      "React", "SQL", "PostgreSQL", "MongoDB", "Git", "spaCy", "Hugging Face",
                      "Transformers", "REST API", "Pandas", "NumPy", "TensorFlow", "Deep Learning",
                      "Computer Vision", "Linux", "Flask"]
    )
