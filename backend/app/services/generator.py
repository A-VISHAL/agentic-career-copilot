"""
LLM-powered Generation Services
Resume rewriting, cover letter generation, interview simulation, and career coaching.
Uses OpenAI API (GPT-4o) with fallback to template-based generation.
"""

import os
import json
from typing import Optional
from ..models.schemas import (
    ResumeImprovement, InterviewQuestion, InterviewFeedback,
    RoadmapItem, CareerRoadmap, ChatMessage, ParsedResume
)
from ..core.config import settings


async def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    """Call OpenAI API for text generation. Falls back to template if no API key."""
    
    if not settings.OPENAI_API_KEY:
        return ""  # Will use fallback templates
    
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=1500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM call error: {e}")
        return ""


# ─── RESUME REWRITING ───

RESUME_REWRITE_SYSTEM = """You are an expert resume writer who specializes in making resumes specific, 
quantified, and authentic. You NEVER produce generic AI-sounding language. 

Rules:
- Replace vague descriptions with specific metrics and outcomes
- Use the candidate's real voice, not corporate jargon
- Add quantified impact (numbers, percentages, dollar amounts)
- Make each bullet tell a story: [Action] → [Method] → [Result]
- ATS-optimize without losing authenticity
- Flag and remove clichéd AI-generated phrases
"""

async def rewrite_resume_bullets(experiences: list[dict], job_context: str = "") -> list[ResumeImprovement]:
    """Rewrite resume bullets to be specific, quantified, and authentic."""
    
    improvements = []
    
    # Template-based improvements (always available)
    template_improvements = [
        ResumeImprovement(
            original="Responsible for developing machine learning models that improved efficiency and performance metrics across various business domains.",
            improved="Built NLP classification pipeline processing 2.3M daily events, reducing false-positive alerts by 41% and saving 120 eng-hours/month.",
            reason="Generic → specific: added exact metrics, real project, quantified outcome",
            impact_area="specificity"
        ),
        ResumeImprovement(
            original="Worked on various projects using Python and helped the team with technical tasks and problem solving.",
            improved="Led 3-person ML team to ship real-time fraud detection model in 6 weeks, blocking $840K in fraudulent transactions in Q1.",
            reason="Vague → quantified: team size, timeline, dollar impact, specific outcome",
            impact_area="metrics"
        ),
        ResumeImprovement(
            original="Experienced in building and deploying APIs and backend services for multiple applications.",
            improved="Designed FastAPI REST endpoints serving 50K+ predictions/day at <100ms p99 latency, supporting 3 production ML models.",
            reason="Abstract → concrete: specific technology, throughput, latency, scale",
            impact_area="clarity"
        ),
        ResumeImprovement(
            original="Skilled in data analysis and creating dashboards to help stakeholders make data-driven decisions.",
            improved="Built real-time model monitoring dashboard tracking drift, accuracy (93% → 96%), and latency across 12 production experiments using Grafana + Prometheus.",
            reason="Passive → active: named tools, showed improvement trajectory, added scale",
            impact_area="keywords"
        )
    ]
    
    # Try LLM for custom improvements
    if experiences and settings.OPENAI_API_KEY:
        for exp in experiences[:3]:
            desc = exp.get("description", "") if isinstance(exp, dict) else getattr(exp, "description", "")
            if desc and len(desc) > 20:
                prompt = f"""Rewrite this resume bullet to be more specific and quantified.
Original: {desc}
Job context: {job_context if job_context else 'General ML/Software role'}

Return JSON: {{"original": "...", "improved": "...", "reason": "...", "impact_area": "specificity"}}"""
                
                result = await call_llm(RESUME_REWRITE_SYSTEM, prompt)
                if result:
                    try:
                        data = json.loads(result)
                        improvements.append(ResumeImprovement(**data))
                    except:
                        pass
    
    # Merge template improvements with LLM ones
    return improvements if improvements else template_improvements


# ─── COVER LETTER GENERATION ───

COVER_LETTER_SYSTEM = """You are an expert cover letter writer. Write in a confident, specific, and 
authentic voice. Avoid generic phrases like "I am excited to apply" or "I believe my skills."

Structure:
1. Opening hook: Connect your specific experience to their specific need
2. Body: 2-3 concrete examples of how your work maps to their requirements
3. Close: Specific next step, not generic enthusiasm

Rules: Be concise (max 250 words). Sound human. Reference the actual job requirements."""

async def generate_cover_letter(resume_text: str, jd_text: str, tone: str = "professional") -> str:
    """Generate a tailored, non-generic cover letter."""
    
    prompt = f"""Write a cover letter for this candidate applying to this role.

RESUME:
{resume_text[:2000]}

JOB DESCRIPTION:
{jd_text[:1500]}

Tone: {tone}
"""
    
    result = await call_llm(COVER_LETTER_SYSTEM, prompt)
    
    if not result:
        # Template fallback
        return f"""Dear Hiring Manager,

Your posting for this role caught my attention because it directly maps to what I've been building for the past 4 years — production ML systems that work at scale, not just in notebooks.

At TechCorp AI Labs, I built an NLP classification pipeline processing 2.3M daily events that reduced false-positive alerts by 41%. The technical stack (Python, PyTorch, FastAPI) and the problem domain align closely with what your team needs.

What I'd bring that's harder to find on a resume: I've shipped models end-to-end, from data pipeline to production API with monitoring. I've led small teams through tight deadlines — our fraud detection model went from concept to production in 6 weeks, blocking $840K in Q1.

I'd love to discuss how my experience with {', '.join(['production ML', 'NLP', 'FastAPI'])} maps to your team's priorities. I'm available for a conversation at your convenience.

Best regards,
Arjun Mehta"""
    
    return result


# ─── INTERVIEW SIMULATOR ───

INTERVIEW_SYSTEM = """You are an expert technical interviewer for the specific role described. 
Generate questions that are:
1. Directly derived from the job description
2. Progressive in difficulty (easy → medium → hard)
3. Mix of technical, behavioral, and system design
4. Focused on practical experience, not textbook knowledge

For feedback, evaluate:
- STAR method usage (Situation, Task, Action, Result)
- Specificity (named tools, quantified outcomes)
- Technical accuracy
- Role relevance"""


DEFAULT_INTERVIEW_QUESTIONS = [
    InterviewQuestion(
        question="Can you walk me through a machine learning system you've built and deployed to production? What were the main technical challenges?",
        category="technical",
        difficulty="medium",
        key_points=["production deployment", "model monitoring", "latency tradeoffs", "A/B testing", "scale challenges"],
        sample_answer="At TechCorp, I built an NLP classification pipeline processing 2.3M events/day. The main challenges were managing model drift (solved with automated retraining triggers), optimizing inference latency from 200ms to <100ms (using model quantization and batched predictions), and building a monitoring dashboard to track accuracy in real-time."
    ),
    InterviewQuestion(
        question="How do you approach the trade-off between model accuracy and inference latency in production?",
        category="technical",
        difficulty="hard",
        key_points=["quantization", "model distillation", "caching", "batching", "latency benchmarks"],
        sample_answer="I think about this as a spectrum. First, I establish latency SLAs with the product team. Then I use techniques like model pruning, quantization (INT8 in our case), and prediction caching for common inputs. For our fraud model, we accepted a 0.3% accuracy drop to cut p99 latency from 180ms to 45ms — the business impact of faster decisions outweighed the marginal accuracy loss."
    ),
    InterviewQuestion(
        question="Tell me about a time you had to convince your team to adopt a different technical approach. What happened?",
        category="behavioral",
        difficulty="medium",
        key_points=["leadership", "data-driven argument", "compromise", "outcome"],
        sample_answer=None
    ),
    InterviewQuestion(
        question="Design a real-time recommendation system that serves 100K users concurrently. Walk me through your architecture.",
        category="system_design",
        difficulty="hard",
        key_points=["caching layers", "feature store", "model serving", "A/B testing infrastructure", "cold start problem"],
        sample_answer=None
    ),
    InterviewQuestion(
        question="What's your approach to monitoring ML models in production? How do you detect and handle model drift?",
        category="technical",
        difficulty="medium",
        key_points=["data drift", "concept drift", "monitoring tools", "retraining triggers", "alerting"],
        sample_answer=None
    )
]


async def generate_interview_questions(jd_text: str, num_questions: int = 5) -> list[InterviewQuestion]:
    """Generate role-specific interview questions from the job description."""
    
    if settings.OPENAI_API_KEY:
        prompt = f"""Generate {num_questions} interview questions for this role:

{jd_text[:1500]}

Return JSON array: [{{"question": "...", "category": "technical|behavioral|system_design", "difficulty": "easy|medium|hard", "key_points": ["..."]}}]"""
        
        result = await call_llm(INTERVIEW_SYSTEM, prompt, temperature=0.8)
        if result:
            try:
                data = json.loads(result)
                return [InterviewQuestion(**q) for q in data]
            except:
                pass
    
    return DEFAULT_INTERVIEW_QUESTIONS[:num_questions]


async def evaluate_interview_answer(question: str, answer: str, jd_context: str = "") -> InterviewFeedback:
    """Evaluate an interview answer and provide detailed feedback."""
    
    if settings.OPENAI_API_KEY:
        prompt = f"""Evaluate this interview answer:

Question: {question}
Answer: {answer}
Role context: {jd_context[:500] if jd_context else 'ML Engineer role'}

Score from 0-100 on:
1. Overall quality
2. Technical depth
3. Clarity and structure

Return JSON: {{"score": N, "technical_depth": N, "clarity": N, "feedback": "...", "strengths": ["..."], "improvements": ["..."], "keywords_used": ["..."], "keywords_missed": ["..."]}}"""
        
        result = await call_llm(INTERVIEW_SYSTEM, prompt)
        if result:
            try:
                data = json.loads(result)
                return InterviewFeedback(**data)
            except:
                pass
    
    # Template-based evaluation
    word_count = len(answer.split())
    has_numbers = bool(re.search(r'\d+', answer))
    has_technical = bool(re.search(r'(?:model|API|deploy|pipeline|data|algorithm|system|scale|latency)', answer, re.IGNORECASE))
    
    score = 40
    tech_depth = 30
    clarity = 50
    
    if word_count > 50:
        score += 15
        clarity += 10
    if word_count > 100:
        score += 10
        clarity += 5
    if has_numbers:
        score += 15
        tech_depth += 20
    if has_technical:
        score += 10
        tech_depth += 20
    
    # Check for STAR method
    star_signals = ['situation', 'task', 'action', 'result', 'challenge', 'outcome', 'impact', 'led', 'built', 'designed']
    star_count = sum(1 for s in star_signals if s.lower() in answer.lower())
    if star_count >= 3:
        score += 10
        clarity += 15
    
    score = min(score, 100)
    tech_depth = min(tech_depth, 100)
    clarity = min(clarity, 100)
    
    strengths = []
    improvements = []
    
    if has_numbers:
        strengths.append("Good use of specific numbers and metrics")
    else:
        improvements.append("Add quantified outcomes (numbers, percentages, timelines)")
    
    if has_technical:
        strengths.append("Demonstrated technical knowledge")
    else:
        improvements.append("Include specific technologies and technical details")
    
    if word_count > 50:
        strengths.append("Sufficient detail in response")
    else:
        improvements.append("Expand your answer with more context and examples")
    
    if star_count >= 3:
        strengths.append("Good STAR method structure")
    else:
        improvements.append("Use the STAR method: Situation, Task, Action, Result")
    
    keywords_expected = ["production", "deployment", "monitoring", "scale", "latency", "testing"]
    keywords_used = [k for k in keywords_expected if k.lower() in answer.lower()]
    keywords_missed = [k for k in keywords_expected if k.lower() not in answer.lower()]
    
    feedback = f"Your answer scored {score}/100. "
    if score >= 80:
        feedback += "Strong response with good technical depth and specificity."
    elif score >= 60:
        feedback += "Decent answer, but could benefit from more specific examples and metrics."
    else:
        feedback += "Consider adding more detail, specific technologies, and quantified outcomes."
    
    return InterviewFeedback(
        score=score,
        technical_depth=tech_depth,
        clarity=clarity,
        feedback=feedback,
        strengths=strengths,
        improvements=improvements,
        keywords_used=keywords_used,
        keywords_missed=keywords_missed
    )


# ─── CAREER ROADMAP ───

async def generate_roadmap(resume: ParsedResume, jd_text: str, match_score: float) -> CareerRoadmap:
    """Generate a personalized career roadmap based on skill gaps."""
    from .matcher import parse_job_description, compute_skill_overlap
    
    jd = parse_job_description(jd_text)
    skill_overlap = compute_skill_overlap(resume.skill_names, jd.required_skills + jd.preferred_skills)
    missing_skills = skill_overlap["missing"]
    
    items = []
    
    # Phase 1: Quick wins (weeks 1-2)
    if missing_skills:
        items.append(RoadmapItem(
            week="Week 1–2",
            title=f"{missing_skills[0]} Fundamentals",
            description=f"Complete a foundational course on {missing_skills[0]}. Apply it to your existing project. This is the highest-ROI action for your target role.",
            category="learn",
            priority="high",
            resources=[f"Official {missing_skills[0]} documentation", "YouTube crash course (free)"]
        ))
    
    # Phase 2: Build (weeks 3-4)
    items.append(RoadmapItem(
        week="Week 3–4",
        title="Deploy a project end-to-end",
        description=f"Build a small project using {', '.join(missing_skills[:2]) if len(missing_skills) >= 2 else 'your skills'}. Deploy it live. This is the portfolio gap recruiters see.",
        category="build",
        priority="high",
        resources=["GitHub portfolio template", "Railway/Render for free deployment"]
    ))
    
    # Phase 3: Apply (weeks 5-6)
    items.append(RoadmapItem(
        week="Week 5–6",
        title=f"Apply to {min(8, 5 + len(missing_skills))} targeted roles",
        description="Use your updated resume and tailored cover letters. Aim for 70%+ match score roles only.",
        category="apply",
        priority="high",
        resources=["NexusCareer job matching", "LinkedIn job alerts"]
    ))
    
    # Phase 4: Deepen (months 2-3)
    if len(missing_skills) > 1:
        items.append(RoadmapItem(
            week="Week 7–8",
            title=f"Deep dive: {missing_skills[1] if len(missing_skills) > 1 else 'Advanced concepts'}",
            description=f"Go beyond basics in {missing_skills[1] if len(missing_skills) > 1 else 'your weakest area'}. Build a more substantial project demonstrating expertise.",
            category="learn",
            priority="medium",
            resources=["Online courses", "Open source contributions"]
        ))
    
    items.append(RoadmapItem(
        week="Month 2–3",
        title="Interview preparation",
        description="Complete system design prep. Practice 2 mock interviews per week with the AI simulator.",
        category="learn",
        priority="medium",
        resources=["NexusCareer Interview Simulator", "System Design resources"]
    ))
    
    items.append(RoadmapItem(
        week="Month 3",
        title="Final push: targeted applications",
        description="Apply to your top-match roles with fully optimized applications and strong interview prep.",
        category="apply",
        priority="high",
        resources=["NexusCareer auto-apply", "Follow-up tracker"]
    ))
    
    # Estimate readiness
    readiness_weeks = 4 + len(missing_skills) * 2
    
    return CareerRoadmap(
        target_role=jd.title or "Target Role",
        current_level="Mid-level" if len(resume.experiences) >= 2 else "Junior",
        items=items,
        estimated_readiness_weeks=readiness_weeks
    )


# ─── CHAT/COACH ───

COACH_SYSTEM = """You are NexusCareer AI, a friendly, expert career coach. You have access to the 
candidate's resume and their target job description. 

Rules:
- Be specific and actionable, never generic
- Reference their actual skills and experience 
- When giving advice, explain the WHY
- Keep responses concise (2-3 paragraphs max)
- Use a warm but professional tone"""


async def chat_with_coach(messages: list[ChatMessage], resume_context: str = "", job_context: str = "") -> str:
    """Chat with the AI career coach."""
    
    system_prompt = COACH_SYSTEM
    if resume_context:
        system_prompt += f"\n\nCandidate's resume:\n{resume_context[:1000]}"
    if job_context:
        system_prompt += f"\n\nTarget job:\n{job_context[:500]}"
    
    user_prompt = messages[-1].content if messages else "Hello!"
    
    result = await call_llm(system_prompt, user_prompt)
    
    if not result:
        # Template fallback
        user_msg = messages[-1].content.lower() if messages else ""
        
        if "interview" in user_msg or "prepare" in user_msg:
            return "Great question! For interview prep, I'd focus on three things: (1) Practice explaining your ML pipeline project — interviewers love hearing about end-to-end systems you've built. (2) Prepare 2-3 STAR stories about technical challenges you've overcome. (3) Review system design fundamentals, especially around ML model serving at scale. Want me to generate some practice questions?"
        elif "resume" in user_msg or "improve" in user_msg:
            return "Looking at your resume, the biggest improvements would be: (1) Quantify every bullet — replace 'improved performance' with 'reduced latency by 41%'. (2) Lead with impact, not responsibilities. (3) Make sure your most relevant experience is front-and-center for your target role. Shall I rewrite specific bullets?"
        elif "skill" in user_msg or "learn" in user_msg:
            return "Based on your skill gaps, I'd prioritize in this order: (1) The missing required skills for your target role — these have the highest impact on your match score. (2) Skills with rising market demand in your area. (3) Skills that complement your existing strengths. Want me to create a personalized learning roadmap?"
        else:
            return "I'm your AI career coach! I can help you with:\n\n• **Resume optimization** — making your bullets specific and impactful\n• **Interview prep** — practicing with role-specific questions\n• **Skill gaps** — identifying what to learn next\n• **Job search strategy** — finding the best matching roles\n\nWhat would you like to work on?"
    
    return result


import re
