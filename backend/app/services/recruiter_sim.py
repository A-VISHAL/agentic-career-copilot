"""
Recruiter Simulation (STEP 8)
Simulates recruiter decision-making process with realistic rejection/acceptance criteria.
"""

from typing import Dict, List
from ..models.schemas import ParsedResume, JobDescription, MatchResult


class RecruiterDecision:
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    MAYBE = "MAYBE"


def simulate_recruiter_review(
    resume: ParsedResume,
    jd: JobDescription,
    match_result: MatchResult
) -> Dict:
    """
    Simulate a recruiter's decision-making process.
    Returns decision, reasoning, and specific feedback.
    """
    
    decision = RecruiterDecision.MAYBE
    reasons = []
    red_flags = []
    green_flags = []
    feedback = []
    
    score = match_result.overall_score
    
    # Extract key metrics
    resume_skills = set(s.lower() for s in resume.skill_names)
    required_skills = set(s.lower() for s in jd.required_skills)
    matched_required = resume_skills & required_skills
    missing_required = required_skills - resume_skills
    
    skill_match_rate = len(matched_required) / max(len(required_skills), 1)
    
    # GREEN FLAGS (positive signals)
    if skill_match_rate >= 0.8:
        green_flags.append("Strong skill alignment (80%+ match)")
    
    if len(resume.experiences) >= 3:
        green_flags.append("Solid work history with multiple roles")
    
    if len(resume.projects) >= 2:
        green_flags.append("Demonstrated hands-on building through projects")
    
    # Check for quantified achievements
    quantified_count = sum(
        1 for exp in resume.experiences
        if any(char.isdigit() for char in exp.description)
    )
    if quantified_count >= 2:
        green_flags.append("Resume includes quantified achievements")
    
    # Check for relevant keywords in experience
    relevant_exp = any(
        any(skill.lower() in exp.description.lower() for skill in jd.required_skills[:5])
        for exp in resume.experiences
    )
    if relevant_exp:
        green_flags.append("Direct experience with required technologies")
    
    # RED FLAGS (negative signals)
    if skill_match_rate < 0.5:
        red_flags.append("Missing 50%+ of required skills")
    
    if len(resume.experiences) == 0:
        red_flags.append("No professional experience listed")
    
    if len(resume.projects) == 0 and len(resume.experiences) < 2:
        red_flags.append("Limited evidence of hands-on technical work")
    
    # Check for generic/weak descriptions
    generic_phrases = ["responsible for", "worked on", "helped with", "various", "multiple"]
    generic_count = sum(
        1 for exp in resume.experiences
        for phrase in generic_phrases
        if phrase in exp.description.lower()
    )
    if generic_count >= 3:
        red_flags.append("Resume contains generic, non-specific language")
    
    # Check for missing metrics
    if quantified_count == 0:
        red_flags.append("No quantified achievements or impact metrics")
    
    # Check for critical missing skills
    critical_skills = ["python", "javascript", "java", "react", "node", "aws", "docker"]
    critical_missing = [
        s for s in missing_required
        if any(crit in s.lower() for crit in critical_skills)
    ]
    if len(critical_missing) >= 2:
        red_flags.append(f"Missing critical skills: {', '.join(critical_missing[:2])}")
    
    # DECISION LOGIC
    if score >= 85 and len(red_flags) <= 1:
        decision = RecruiterDecision.ACCEPT
        reasons = [
            "Strong overall match score (85%+)",
            "Meets most required qualifications",
            "Profile aligns well with role requirements"
        ]
        feedback = [
            "Your profile is a strong match for this role",
            "Recommend moving forward to phone screen",
            "Prepare to discuss specific projects and achievements"
        ]
    
    elif score >= 70 and len(red_flags) <= 2:
        decision = RecruiterDecision.MAYBE
        reasons = [
            "Decent match but with some gaps",
            "Profile shows potential but needs strengthening",
            "Some required skills are missing"
        ]
        feedback = [
            "You're on the borderline for this role",
            "Address the skill gaps to improve your chances",
            "Consider applying after gaining more relevant experience"
        ]
    
    else:
        decision = RecruiterDecision.REJECT
        reasons = [
            "Match score below threshold (< 70%)",
            "Significant skill gaps identified",
            "Profile doesn't align with role requirements"
        ]
        feedback = [
            "Your profile doesn't meet the minimum requirements",
            "Focus on building the missing skills before applying",
            "Consider roles that better match your current skillset"
        ]
    
    # Add specific feedback based on flags
    if red_flags:
        feedback.append(f"Key concerns: {'; '.join(red_flags[:3])}")
    
    if green_flags:
        feedback.append(f"Strengths: {'; '.join(green_flags[:3])}")
    
    # Time to review (realistic simulation)
    import random
    review_time_seconds = random.randint(45, 180)  # 45s to 3min
    
    # Likelihood of getting interview
    if decision == RecruiterDecision.ACCEPT:
        interview_likelihood = min(85 + (score - 85) * 0.5, 95)
    elif decision == RecruiterDecision.MAYBE:
        interview_likelihood = 40 + (score - 70) * 1.5
    else:
        interview_likelihood = max(5, score * 0.3)
    
    return {
        "decision": decision,
        "confidence": round(min(score, 95), 1),
        "reasons": reasons,
        "red_flags": red_flags,
        "green_flags": green_flags,
        "feedback": feedback,
        "review_time_seconds": review_time_seconds,
        "interview_likelihood": round(interview_likelihood, 1),
        "next_steps": get_next_steps(decision, red_flags, green_flags),
        "recruiter_notes": generate_recruiter_notes(
            resume, jd, decision, score, red_flags, green_flags
        )
    }


def get_next_steps(decision: str, red_flags: List[str], green_flags: List[str]) -> List[str]:
    """Generate actionable next steps based on decision."""
    
    if decision == RecruiterDecision.ACCEPT:
        return [
            "Prepare for phone screen interview",
            "Review the job description in detail",
            "Prepare STAR stories for your key achievements",
            "Research the company and team",
            "Prepare questions to ask the interviewer"
        ]
    
    elif decision == RecruiterDecision.MAYBE:
        return [
            "Strengthen your resume with quantified achievements",
            "Address the top 2-3 skill gaps",
            "Build a project demonstrating missing skills",
            "Reapply in 2-3 months after improvements",
            "Consider similar roles with better match scores"
        ]
    
    else:  # REJECT
        return [
            "Focus on building the missing required skills",
            "Gain more relevant experience (6-12 months)",
            "Build 2-3 portfolio projects in the target domain",
            "Target roles with 70%+ match score instead",
            "Consider junior/mid-level positions if applicable"
        ]


def generate_recruiter_notes(
    resume: ParsedResume,
    jd: JobDescription,
    decision: str,
    score: float,
    red_flags: List[str],
    green_flags: List[str]
) -> str:
    """
    Generate realistic recruiter notes (what they'd write internally).
    """
    
    name = resume.name or "Candidate"
    role = jd.title or "the role"
    
    if decision == RecruiterDecision.ACCEPT:
        notes = f"{name} - Strong match for {role}. "
        notes += f"Match score: {score}%. "
        if green_flags:
            notes += f"Highlights: {', '.join(green_flags[:2])}. "
        notes += "Recommend phone screen. "
        notes += "Focus interview on: technical depth, system design, team fit."
    
    elif decision == RecruiterDecision.MAYBE:
        notes = f"{name} - Borderline for {role}. "
        notes += f"Match score: {score}%. "
        if red_flags:
            notes += f"Concerns: {', '.join(red_flags[:2])}. "
        if green_flags:
            notes += f"Positives: {', '.join(green_flags[:1])}. "
        notes += "Hold for now. Revisit if stronger candidates don't emerge."
    
    else:  # REJECT
        notes = f"{name} - Not a fit for {role}. "
        notes += f"Match score: {score}%. "
        if red_flags:
            notes += f"Key gaps: {', '.join(red_flags[:3])}. "
        notes += "Recommend rejection. "
        notes += "Suggest candidate builds more experience before reapplying."
    
    return notes


def simulate_ats_screening(resume: ParsedResume, jd: JobDescription) -> Dict:
    """
    Simulate ATS (Applicant Tracking System) keyword screening.
    This happens BEFORE human review.
    """
    
    # Extract keywords from JD
    jd_keywords = set(s.lower() for s in jd.required_skills + jd.preferred_skills)
    
    # Extract keywords from resume
    resume_keywords = set(s.lower() for s in resume.skill_names)
    
    # Calculate keyword match
    matched_keywords = jd_keywords & resume_keywords
    missing_keywords = jd_keywords - resume_keywords
    
    keyword_match_rate = len(matched_keywords) / max(len(jd_keywords), 1)
    
    # ATS pass/fail threshold (typically 60-70%)
    ats_threshold = 0.60
    passed_ats = keyword_match_rate >= ats_threshold
    
    return {
        "passed_ats": passed_ats,
        "keyword_match_rate": round(keyword_match_rate * 100, 1),
        "matched_keywords": list(matched_keywords)[:10],
        "missing_keywords": list(missing_keywords)[:10],
        "threshold": ats_threshold * 100,
        "recommendation": (
            "Resume likely to pass ATS screening" if passed_ats
            else "Resume may be filtered out by ATS - add missing keywords"
        )
    }
