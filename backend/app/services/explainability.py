"""
Explainability Layer (STEP 5)
Uses SHAP-like attribution and DiCE-like counterfactuals for XAI.
"""

from typing import Dict, List, Tuple
import numpy as np
from ..models.schemas import ParsedResume, JobDescription, MatchResult


def compute_shap_values(
    resume: ParsedResume,
    jd: JobDescription,
    match_result: MatchResult
) -> Dict[str, any]:
    """
    Compute SHAP-like feature attributions.
    Identifies which features contribute positively or negatively to the match score.
    """
    
    # Extract features
    resume_skills = set(s.lower() for s in resume.skill_names)
    jd_required = set(s.lower() for s in jd.required_skills)
    jd_preferred = set(s.lower() for s in jd.preferred_skills)
    
    # Positive contributors (matched skills)
    matched_required = resume_skills & jd_required
    matched_preferred = resume_skills & jd_preferred
    
    # Negative contributors (missing skills)
    missing_required = jd_required - resume_skills
    missing_preferred = jd_preferred - resume_skills
    
    # Calculate SHAP values (contribution to score)
    positive_features = []
    negative_features = []
    
    # Matched required skills have high positive impact
    for skill in matched_required:
        # Find original case
        original_skill = next((s for s in resume.skill_names if s.lower() == skill), skill)
        positive_features.append({
            "feature": original_skill,
            "shap_value": 0.15,  # High impact
            "reason": "Required skill matched"
        })
    
    # Matched preferred skills have medium positive impact
    for skill in matched_preferred:
        original_skill = next((s for s in resume.skill_names if s.lower() == skill), skill)
        positive_features.append({
            "feature": original_skill,
            "shap_value": 0.08,  # Medium impact
            "reason": "Preferred skill matched"
        })
    
    # Experience contributes positively
    if len(resume.experiences) >= 2:
        positive_features.append({
            "feature": f"{len(resume.experiences)} years experience",
            "shap_value": 0.12,
            "reason": "Sufficient work experience"
        })
    
    # Projects contribute positively
    if len(resume.projects) > 0:
        positive_features.append({
            "feature": f"{len(resume.projects)} projects",
            "shap_value": 0.10,
            "reason": "Demonstrated hands-on building"
        })
    
    # Missing required skills have high negative impact
    for skill in missing_required:
        original_skill = next((s for s in jd.required_skills if s.lower() == skill), skill)
        negative_features.append({
            "feature": f"Missing: {original_skill}",
            "shap_value": -0.18,  # High negative impact
            "reason": "Required skill not found in resume"
        })
    
    # Missing preferred skills have low negative impact
    for skill in list(missing_preferred)[:3]:  # Limit to top 3
        original_skill = next((s for s in jd.preferred_skills if s.lower() == skill), skill)
        negative_features.append({
            "feature": f"Missing: {original_skill}",
            "shap_value": -0.05,  # Low negative impact
            "reason": "Preferred skill not found"
        })
    
    # Sort by absolute impact
    positive_features.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
    negative_features.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
    
    return {
        "positive_features": positive_features[:8],  # Top 8 positive
        "negative_features": negative_features[:8],  # Top 8 negative
        "base_score": 50.0,  # Baseline score
        "total_positive_contribution": sum(f["shap_value"] for f in positive_features),
        "total_negative_contribution": sum(f["shap_value"] for f in negative_features)
    }


def generate_dice_counterfactuals(
    resume: ParsedResume,
    jd: JobDescription,
    current_score: float,
    shap_analysis: Dict
) -> List[Dict]:
    """
    Generate DiCE-like counterfactual explanations.
    "If you change X, your score would become Y"
    """
    
    counterfactuals = []
    
    # Extract missing skills from negative features
    missing_skills = [
        f["feature"].replace("Missing: ", "")
        for f in shap_analysis["negative_features"]
        if f["feature"].startswith("Missing:")
    ]
    
    # Counterfactual 1: Add single high-impact skill
    if missing_skills:
        skill = missing_skills[0]
        impact = abs(shap_analysis["negative_features"][0]["shap_value"]) * 100
        projected = min(current_score + impact, 98)
        
        counterfactuals.append({
            "change": f"Add '{skill}' to your skillset",
            "current_score": round(current_score, 1),
            "projected_score": round(projected, 1),
            "delta": round(projected - current_score, 1),
            "feasibility": "medium",
            "timeline": "2-4 weeks",
            "action_items": [
                f"Complete online course on {skill}",
                f"Build a small project using {skill}",
                f"Add {skill} to resume with project context"
            ]
        })
    
    # Counterfactual 2: Add multiple skills
    if len(missing_skills) >= 2:
        skills = missing_skills[:2]
        combined_impact = sum(
            abs(f["shap_value"]) * 100
            for f in shap_analysis["negative_features"][:2]
        )
        projected = min(current_score + combined_impact, 97)
        
        counterfactuals.append({
            "change": f"Add '{skills[0]}' + '{skills[1]}' with a deployed project",
            "current_score": round(current_score, 1),
            "projected_score": round(projected, 1),
            "delta": round(projected - current_score, 1),
            "feasibility": "medium",
            "timeline": "4-6 weeks",
            "action_items": [
                f"Learn {skills[0]} and {skills[1]} fundamentals",
                f"Build and deploy a project using both technologies",
                "Document the project with metrics and outcomes",
                "Update resume with quantified results"
            ]
        })
    
    # Counterfactual 3: Add experience
    if len(resume.experiences) < 3:
        projected = min(current_score + 12, 95)
        counterfactuals.append({
            "change": "Add 1 more year of relevant experience",
            "current_score": round(current_score, 1),
            "projected_score": round(projected, 1),
            "delta": round(projected - current_score, 1),
            "feasibility": "low",
            "timeline": "12 months",
            "action_items": [
                "Gain experience through current role",
                "Take on side projects or freelance work",
                "Contribute to open source projects"
            ]
        })
    
    # Counterfactual 4: Add project
    if len(resume.projects) < 2:
        projected = min(current_score + 8, 92)
        counterfactuals.append({
            "change": "Add 1 production-level project to portfolio",
            "current_score": round(current_score, 1),
            "projected_score": round(projected, 1),
            "delta": round(projected - current_score, 1),
            "feasibility": "high",
            "timeline": "2-3 weeks",
            "action_items": [
                "Build a project addressing a real problem",
                "Deploy it with live URL",
                "Add metrics: users, performance, impact",
                "Write detailed README with architecture"
            ]
        })
    
    # Counterfactual 5: Optimize resume (quick win)
    projected = min(current_score + 5, 90)
    counterfactuals.append({
        "change": "Rewrite resume bullets with metrics and impact",
        "current_score": round(current_score, 1),
        "projected_score": round(projected, 1),
        "delta": round(projected - current_score, 1),
        "feasibility": "high",
        "timeline": "1-2 hours",
        "action_items": [
            "Add numbers to every bullet point",
            "Use action verbs (Built, Led, Reduced)",
            "Quantify impact (%, $, time saved)",
            "Remove generic phrases"
        ]
    })
    
    # Sort by delta (highest impact first)
    counterfactuals.sort(key=lambda x: x["delta"], reverse=True)
    
    return counterfactuals


def generate_explainability_report(
    resume: ParsedResume,
    jd: JobDescription,
    match_result: MatchResult
) -> Dict:
    """
    Generate complete explainability report combining SHAP and DiCE.
    """
    
    # Compute SHAP values
    shap_analysis = compute_shap_values(resume, jd, match_result)
    
    # Generate counterfactuals
    counterfactuals = generate_dice_counterfactuals(
        resume, jd, match_result.overall_score, shap_analysis
    )
    
    # Create summary
    top_positive = shap_analysis["positive_features"][:3]
    top_negative = shap_analysis["negative_features"][:3]
    
    summary = {
        "why_matched": [f["feature"] for f in top_positive],
        "why_not_matched": [f["feature"] for f in top_negative],
        "quick_wins": [c for c in counterfactuals if c["feasibility"] == "high"][:2],
        "highest_impact": counterfactuals[0] if counterfactuals else None
    }
    
    return {
        "shap_analysis": shap_analysis,
        "counterfactuals": counterfactuals,
        "summary": summary,
        "visualization_data": {
            "positive_bars": [
                {"label": f["feature"], "value": f["shap_value"] * 100}
                for f in top_positive
            ],
            "negative_bars": [
                {"label": f["feature"], "value": f["shap_value"] * 100}
                for f in top_negative
            ]
        }
    }
