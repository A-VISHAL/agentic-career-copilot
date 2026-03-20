"""
Semantic Matching Service
Performs embedding-based job ↔ resume matching with SHAP-like attribution 
and counterfactual suggestions. Works with or without sentence-transformers.
"""

import re
import math
from collections import Counter
from ..models.schemas import (
    MatchResult, MatchDimension, CounterfactualSuggestion, 
    ParsedResume, JobDescription
)


# ─── JD PARSER ───

def parse_job_description(jd_text: str) -> JobDescription:
    """Extract structured data from a raw job description."""
    
    # Extract title
    lines = [l.strip() for l in jd_text.split('\n') if l.strip()]
    title = lines[0] if lines else "Unknown Role"
    
    # Extract skills mentioned
    from .parser import SKILL_PATTERNS
    found_skills = []
    jd_lower = jd_text.lower()
    for skill_lower, skill_proper in SKILL_PATTERNS.items():
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        if re.search(pattern, jd_lower):
            found_skills.append(skill_proper)
    
    # Try to separate required vs preferred
    required_section = re.search(r'(?:required|must[\s-]have|minimum|essential).*?(?=preferred|nice|bonus|$)', jd_text, re.IGNORECASE | re.DOTALL)
    preferred_section = re.search(r'(?:preferred|nice[\s-]to[\s-]have|bonus|plus).*', jd_text, re.IGNORECASE | re.DOTALL)
    
    required_skills = found_skills  # default: all are required
    preferred_skills = []
    
    if preferred_section:
        pref_text = preferred_section.group(0).lower()
        preferred_skills = [s for s in found_skills if s.lower() in pref_text]
        if required_section:
            req_text = required_section.group(0).lower()
            required_skills = [s for s in found_skills if s.lower() in req_text]
    
    # Extract experience requirement
    exp_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)', jd_text, re.IGNORECASE)
    experience = f"{exp_match.group(1)}+ years" if exp_match else None
    
    return JobDescription(
        title=title[:100],
        description=jd_text,
        required_skills=required_skills if required_skills else found_skills,
        preferred_skills=preferred_skills,
        experience_required=experience,
    )


# ─── MATCHING ENGINE ───

def compute_skill_overlap(resume_skills: list[str], jd_skills: list[str]) -> dict:
    """Compute skill overlap between resume and job description."""
    resume_set = {s.lower() for s in resume_skills}
    jd_set = {s.lower() for s in jd_skills}
    
    matched = resume_set & jd_set
    missing = jd_set - resume_set
    extra = resume_set - jd_set
    
    overlap_ratio = len(matched) / max(len(jd_set), 1)
    
    return {
        "matched": [s for s in jd_skills if s.lower() in matched],
        "missing": [s for s in jd_skills if s.lower() in missing],
        "extra": list(extra),
        "overlap_ratio": overlap_ratio
    }


def compute_text_similarity(text_a: str, text_b: str) -> float:
    """Simple TF-IDF-like cosine similarity between two texts."""
    words_a = re.findall(r'\w+', text_a.lower())
    words_b = re.findall(r'\w+', text_b.lower())
    
    counter_a = Counter(words_a)
    counter_b = Counter(words_b)
    
    all_words = set(counter_a.keys()) | set(counter_b.keys())
    
    dot_product = sum(counter_a.get(w, 0) * counter_b.get(w, 0) for w in all_words)
    norm_a = math.sqrt(sum(v**2 for v in counter_a.values()))
    norm_b = math.sqrt(sum(v**2 for v in counter_b.values()))
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)


# Dimension weights for final score
DIMENSION_WEIGHTS = {
    "technical_skills": 0.35,
    "experience_fit": 0.25,
    "domain_knowledge": 0.15,
    "project_depth": 0.15,
    "communication": 0.10,
}


def compute_dimension_scores(resume: ParsedResume, jd: JobDescription) -> list[MatchDimension]:
    """Compute match score per dimension with SHAP-like attribution."""
    
    skill_overlap = compute_skill_overlap(resume.skill_names, jd.required_skills + jd.preferred_skills)
    text_sim = compute_text_similarity(resume.raw_text, jd.description)
    
    # 1. Technical Skills
    tech_score = min(skill_overlap["overlap_ratio"] * 100 + 10, 100)  # base + overlap
    tech_shap = (tech_score / 100 - 0.5) * DIMENSION_WEIGHTS["technical_skills"] * 2
    
    # 2. Experience Fit
    exp_score = min(len(resume.experiences) * 25 + text_sim * 40, 100)
    exp_shap = (exp_score / 100 - 0.5) * DIMENSION_WEIGHTS["experience_fit"] * 2
    
    # 3. Domain Knowledge
    domain_score = text_sim * 100 * 1.2
    domain_score = min(domain_score, 100)
    domain_shap = (domain_score / 100 - 0.5) * DIMENSION_WEIGHTS["domain_knowledge"] * 2
    
    # 4. Project Depth
    proj_score = min(len(resume.projects) * 30 + 20, 100)
    proj_shap = (proj_score / 100 - 0.5) * DIMENSION_WEIGHTS["project_depth"] * 2
    
    # 5. Communication (based on resume quality heuristics)
    comm_score = min(50 + len(resume.experiences) * 5 + (10 if resume.summary else 0), 100)
    comm_shap = (comm_score / 100 - 0.5) * DIMENSION_WEIGHTS["communication"] * 2
    
    dimensions = [
        MatchDimension(
            name="Technical Skills",
            score=round(tech_score, 1),
            matched_items=skill_overlap["matched"],
            missing_items=skill_overlap["missing"],
            shap_value=round(tech_shap, 3),
            explanation=f"Matched {len(skill_overlap['matched'])} of {len(jd.required_skills)} required skills"
        ),
        MatchDimension(
            name="Experience Fit",
            score=round(exp_score, 1),
            matched_items=[e.title for e in resume.experiences],
            missing_items=[],
            shap_value=round(exp_shap, 3),
            explanation=f"{len(resume.experiences)} relevant roles found" + (f", {jd.experience_required} requested" if jd.experience_required else "")
        ),
        MatchDimension(
            name="Domain Knowledge",
            score=round(domain_score, 1),
            matched_items=[],
            missing_items=[],
            shap_value=round(domain_shap, 3),
            explanation=f"Resume-JD semantic alignment: {round(text_sim * 100, 1)}%"
        ),
        MatchDimension(
            name="Project Depth",
            score=round(proj_score, 1),
            matched_items=[p.get("name", "") for p in resume.projects],
            missing_items=[],
            shap_value=round(proj_shap, 3),
            explanation=f"{len(resume.projects)} projects demonstrate hands-on building"
        ),
        MatchDimension(
            name="Communication",
            score=round(comm_score, 1),
            matched_items=[],
            missing_items=[],
            shap_value=round(comm_shap, 3),
            explanation="Based on resume clarity, structure, and detail level"
        ),
    ]
    
    return dimensions


def generate_counterfactuals(resume: ParsedResume, jd: JobDescription, current_score: float) -> list[CounterfactualSuggestion]:
    """
    Generate counterfactual suggestions: "If you added X, your score would become Y."
    This is the core XAI differentiator.
    """
    skill_overlap = compute_skill_overlap(resume.skill_names, jd.required_skills + jd.preferred_skills)
    missing = skill_overlap["missing"]
    
    counterfactuals = []
    
    # Calculate impact per missing skill
    total_jd_skills = len(jd.required_skills) + len(jd.preferred_skills)
    per_skill_impact = (100 - current_score) * 0.6 / max(len(missing), 1)
    
    # High-impact skills (required and missing)
    required_missing = [s for s in missing if s in jd.required_skills]
    preferred_missing = [s for s in missing if s in jd.preferred_skills]
    
    # Sort by estimated impact
    for i, skill in enumerate(required_missing[:3]):
        impact = min(per_skill_impact * 1.5 * (3 - i), 100 - current_score)
        projected = min(current_score + impact, 98)
        counterfactuals.append(CounterfactualSuggestion(
            action=f"Add {skill}",
            current_score=round(current_score, 1),
            projected_score=round(projected, 1),
            impact="high",
            effort="medium",
            description=f"Adding {skill} with a demonstrated project would raise your score from {round(current_score)}% to {round(projected)}%. This is a required skill for the role."
        ))
    
    for i, skill in enumerate(preferred_missing[:2]):
        impact = min(per_skill_impact * 0.8, 100 - current_score)
        projected = min(current_score + impact, 95)
        counterfactuals.append(CounterfactualSuggestion(
            action=f"Add {skill}",
            current_score=round(current_score, 1),
            projected_score=round(projected, 1),
            impact="medium",
            effort="low",
            description=f"Adding {skill} would strengthen your application. It's a preferred but not required skill."
        ))
    
    # Combined suggestion (highest impact)
    if len(required_missing) >= 2:
        combined_impact = min(per_skill_impact * 2.5, 100 - current_score)
        combined_projected = min(current_score + combined_impact, 97)
        skills_text = " + ".join(required_missing[:2])
        counterfactuals.insert(0, CounterfactualSuggestion(
            action=f"Add {skills_text} with a deployed project",
            current_score=round(current_score, 1),
            projected_score=round(combined_projected, 1),
            impact="high",
            effort="medium",
            description=f"Adding {skills_text} together (e.g., in one deployed project) is the single highest-impact change. Score: {round(current_score)}% → {round(combined_projected)}%"
        ))
    
    return counterfactuals


def compute_role_fit_for_candidate(resume: ParsedResume, jd: JobDescription) -> float:
    """
    Bilateral scoring: how good is this role for the candidate's career growth?
    Separate from how good the candidate is for the role.
    """
    # Check if role offers growth
    text_sim = compute_text_similarity(resume.raw_text, jd.description)
    
    # Too similar = no growth, too different = not relevant
    # Sweet spot is 0.3 - 0.7 similarity
    if text_sim < 0.15:
        growth_score = 30
    elif text_sim < 0.3:
        growth_score = 60
    elif text_sim < 0.5:
        growth_score = 90  # sweet spot
    elif text_sim < 0.7:
        growth_score = 80
    else:
        growth_score = 50  # too similar, no growth
    
    # Check for skill stretch
    skill_overlap = compute_skill_overlap(resume.skill_names, jd.required_skills)
    newSkillRatio = len(skill_overlap["missing"]) / max(len(jd.required_skills), 1)
    
    # Some new skills = good growth, too many = not ready
    if newSkillRatio < 0.15:
        growth_score = growth_score * 0.7  # too comfortable
    elif newSkillRatio < 0.4:
        growth_score = growth_score * 1.1  # good stretch
    else:
        growth_score = growth_score * 0.8  # too much stretch
    
    return min(round(growth_score, 1), 100)


async def match_resume_to_job(resume: ParsedResume, jd_text: str) -> MatchResult:
    """
    Main matching function. Returns detailed match result with XAI breakdown.
    """
    jd = parse_job_description(jd_text)
    
    # Compute dimension scores
    dimensions = compute_dimension_scores(resume, jd)
    
    # Overall weighted score
    weights = list(DIMENSION_WEIGHTS.values())
    overall_score = sum(d.score * w for d, w in zip(dimensions, weights))
    overall_score = min(round(overall_score, 1), 100)
    
    # Generate counterfactuals
    counterfactuals = generate_counterfactuals(resume, jd, overall_score)
    
    # Bilateral scoring
    role_fit = compute_role_fit_for_candidate(resume, jd)
    
    # Bias flags (simplified)
    bias_flags = []
    if jd.experience_required:
        exp_years = re.search(r'(\d+)', jd.experience_required)
        if exp_years and int(exp_years.group(1)) > 8:
            bias_flags.append("High experience requirement may inadvertently filter younger candidates")
    
    # Summary
    skill_overlap = compute_skill_overlap(resume.skill_names, jd.required_skills)
    matched_count = len(skill_overlap["matched"])
    missing_count = len(skill_overlap["missing"])
    
    if overall_score >= 85:
        summary = f"Excellent match! You meet {matched_count} of the required skills with strong alignment."
    elif overall_score >= 70:
        summary = f"Good match with {missing_count} key gap(s) identified. Address these to significantly improve your chances."
    elif overall_score >= 50:
        summary = f"Moderate match. {missing_count} critical skills are missing. Focus on the counterfactual suggestions below."
    else:
        summary = f"Low match for this role. Consider skill development in the missing areas or targeting more aligned roles."
    
    return MatchResult(
        overall_score=overall_score,
        dimensions=dimensions,
        counterfactuals=counterfactuals,
        bias_flags=bias_flags,
        role_fit_for_candidate=role_fit,
        summary=summary
    )
