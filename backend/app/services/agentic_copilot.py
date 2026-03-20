"""
Agentic Career Copilot (STEP 10)
Implements autonomous workflow: analyze → plan → improve → generate → track
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum
from ..models.schemas import ParsedResume, JobDescription


class AgentState(str, Enum):
    ANALYZING = "analyzing"
    PLANNING = "planning"
    IMPROVING = "improving"
    GENERATING = "generating"
    TRACKING = "tracking"
    COMPLETED = "completed"


class ApplicationStatus(str, Enum):
    DRAFT = "draft"
    READY = "ready"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class AgenticWorkflow:
    """
    Simulates an agentic workflow for career management.
    This would integrate with LangGraph or CrewAI in production.
    """
    
    def __init__(self):
        self.state = AgentState.ANALYZING
        self.workflow_history = []
        self.applications = []
        self.reminders = []
    
    def analyze_profile(self, resume: ParsedResume, target_roles: List[str]) -> Dict:
        """
        STEP 1: Analyze candidate profile and career goals.
        """
        self.state = AgentState.ANALYZING
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "state": self.state,
            "profile_summary": {
                "total_skills": len(resume.skills),
                "years_experience": len(resume.experiences),
                "projects_count": len(resume.projects),
                "education_level": resume.education[0].degree if resume.education else "Not specified"
            },
            "career_level": self._determine_career_level(resume),
            "strengths": self._identify_strengths(resume),
            "gaps": self._identify_gaps(resume),
            "target_roles": target_roles,
            "recommended_actions": []
        }
        
        self.workflow_history.append({
            "step": "analyze",
            "timestamp": datetime.now().isoformat(),
            "output": analysis
        })
        
        return analysis
    
    def create_action_plan(self, analysis: Dict, target_jd: Optional[JobDescription] = None) -> Dict:
        """
        STEP 2: Create personalized action plan.
        """
        self.state = AgentState.PLANNING
        
        plan = {
            "timestamp": datetime.now().isoformat(),
            "state": self.state,
            "phases": [],
            "timeline_weeks": 0,
            "success_metrics": []
        }
        
        # Phase 1: Immediate improvements (Week 1-2)
        phase1 = {
            "phase": "Immediate Improvements",
            "duration": "1-2 weeks",
            "tasks": [
                {
                    "task": "Optimize resume with metrics",
                    "priority": "high",
                    "estimated_hours": 3,
                    "impact": "high"
                },
                {
                    "task": "Update LinkedIn profile",
                    "priority": "high",
                    "estimated_hours": 2,
                    "impact": "medium"
                },
                {
                    "task": "Prepare elevator pitch",
                    "priority": "medium",
                    "estimated_hours": 1,
                    "impact": "medium"
                }
            ]
        }
        plan["phases"].append(phase1)
        
        # Phase 2: Skill development (Week 3-6)
        if analysis.get("gaps"):
            phase2 = {
                "phase": "Skill Development",
                "duration": "3-6 weeks",
                "tasks": []
            }
            for gap in analysis["gaps"][:3]:
                phase2["tasks"].append({
                    "task": f"Learn {gap}",
                    "priority": "high",
                    "estimated_hours": 20,
                    "impact": "high"
                })
            plan["phases"].append(phase2)
        
        # Phase 3: Portfolio building (Week 7-10)
        phase3 = {
            "phase": "Portfolio Building",
            "duration": "3-4 weeks",
            "tasks": [
                {
                    "task": "Build and deploy 1-2 projects",
                    "priority": "high",
                    "estimated_hours": 40,
                    "impact": "high"
                },
                {
                    "task": "Write technical blog posts",
                    "priority": "medium",
                    "estimated_hours": 8,
                    "impact": "medium"
                }
            ]
        }
        plan["phases"].append(phase3)
        
        # Phase 4: Application campaign (Week 11-12)
        phase4 = {
            "phase": "Application Campaign",
            "duration": "2 weeks",
            "tasks": [
                {
                    "task": "Apply to 15-20 targeted roles",
                    "priority": "high",
                    "estimated_hours": 15,
                    "impact": "high"
                },
                {
                    "task": "Network with 10 people in target companies",
                    "priority": "high",
                    "estimated_hours": 10,
                    "impact": "high"
                },
                {
                    "task": "Prepare for interviews",
                    "priority": "high",
                    "estimated_hours": 20,
                    "impact": "high"
                }
            ]
        }
        plan["phases"].append(phase4)
        
        plan["timeline_weeks"] = 12
        plan["success_metrics"] = [
            "Resume match score > 75% for target roles",
            "3+ interview invitations within 4 weeks",
            "1+ job offer within 12 weeks"
        ]
        
        self.workflow_history.append({
            "step": "plan",
            "timestamp": datetime.now().isoformat(),
            "output": plan
        })
        
        return plan
    
    def track_applications(self) -> Dict:
        """
        STEP 3: Track job applications and follow-ups.
        """
        self.state = AgentState.TRACKING
        
        # Generate sample applications for demo
        if not self.applications:
            self.applications = self._generate_sample_applications()
        
        # Generate reminders
        self.reminders = self._generate_reminders()
        
        tracking = {
            "timestamp": datetime.now().isoformat(),
            "state": self.state,
            "total_applications": len(self.applications),
            "by_status": self._count_by_status(),
            "applications": self.applications,
            "reminders": self.reminders,
            "metrics": {
                "response_rate": self._calculate_response_rate(),
                "interview_rate": self._calculate_interview_rate(),
                "avg_days_to_response": 7.5
            }
        }
        
        self.workflow_history.append({
            "step": "track",
            "timestamp": datetime.now().isoformat(),
            "output": tracking
        })
        
        return tracking
    
    def simulate_interview_prep(self, job_title: str) -> Dict:
        """
        STEP 4: Simulate interview preparation.
        """
        
        prep = {
            "timestamp": datetime.now().isoformat(),
            "job_title": job_title,
            "preparation_plan": {
                "technical_prep": [
                    "Review data structures and algorithms",
                    "Practice system design problems",
                    "Prepare code samples from past projects"
                ],
                "behavioral_prep": [
                    "Prepare 5 STAR stories",
                    "Research company culture and values",
                    "Prepare questions for interviewer"
                ],
                "mock_interviews": [
                    {
                        "type": "Technical",
                        "duration": "45 min",
                        "scheduled": (datetime.now() + timedelta(days=2)).isoformat()
                    },
                    {
                        "type": "Behavioral",
                        "duration": "30 min",
                        "scheduled": (datetime.now() + timedelta(days=3)).isoformat()
                    }
                ]
            },
            "resources": [
                "LeetCode premium",
                "System Design Primer",
                "Behavioral interview guide"
            ]
        }
        
        return prep
    
    def get_workflow_status(self) -> Dict:
        """
        Get current workflow status and history.
        """
        return {
            "current_state": self.state,
            "workflow_history": self.workflow_history,
            "total_steps_completed": len(self.workflow_history),
            "applications_tracked": len(self.applications),
            "pending_reminders": len([r for r in self.reminders if not r.get("completed")])
        }
    
    # Helper methods
    
    def _determine_career_level(self, resume: ParsedResume) -> str:
        exp_count = len(resume.experiences)
        if exp_count == 0:
            return "Entry Level"
        elif exp_count <= 2:
            return "Junior"
        elif exp_count <= 4:
            return "Mid-Level"
        else:
            return "Senior"
    
    def _identify_strengths(self, resume: ParsedResume) -> List[str]:
        strengths = []
        
        if len(resume.skills) >= 10:
            strengths.append("Diverse technical skillset")
        
        if len(resume.projects) >= 2:
            strengths.append("Strong portfolio of projects")
        
        if len(resume.experiences) >= 3:
            strengths.append("Solid work experience")
        
        # Check for quantified achievements
        quantified = sum(
            1 for exp in resume.experiences
            if any(char.isdigit() for char in exp.description)
        )
        if quantified >= 2:
            strengths.append("Quantified achievements")
        
        return strengths
    
    def _identify_gaps(self, resume: ParsedResume) -> List[str]:
        gaps = []
        
        if len(resume.projects) == 0:
            gaps.append("No portfolio projects")
        
        if len(resume.experiences) < 2:
            gaps.append("Limited work experience")
        
        # Check for missing common skills
        common_skills = ["git", "docker", "aws", "testing", "ci/cd"]
        resume_skills_lower = [s.lower() for s in resume.skill_names]
        missing_common = [s for s in common_skills if s not in resume_skills_lower]
        
        if missing_common:
            gaps.extend(missing_common[:3])
        
        return gaps
    
    def _generate_sample_applications(self) -> List[Dict]:
        """Generate sample applications for demo."""
        now = datetime.now()
        
        return [
            {
                "id": "app_001",
                "company": "TechCorp",
                "role": "Senior ML Engineer",
                "status": ApplicationStatus.INTERVIEW_SCHEDULED,
                "applied_date": (now - timedelta(days=14)).isoformat(),
                "last_update": (now - timedelta(days=2)).isoformat(),
                "match_score": 87,
                "interview_date": (now + timedelta(days=3)).isoformat(),
                "notes": "Phone screen went well, technical round scheduled"
            },
            {
                "id": "app_002",
                "company": "DataFlow Inc",
                "role": "ML Engineer",
                "status": ApplicationStatus.UNDER_REVIEW,
                "applied_date": (now - timedelta(days=10)).isoformat(),
                "last_update": (now - timedelta(days=10)).isoformat(),
                "match_score": 82,
                "notes": "Application submitted, awaiting response"
            },
            {
                "id": "app_003",
                "company": "AI Startup",
                "role": "ML Engineer",
                "status": ApplicationStatus.REJECTED,
                "applied_date": (now - timedelta(days=21)).isoformat(),
                "last_update": (now - timedelta(days=7)).isoformat(),
                "match_score": 75,
                "notes": "Rejected - looking for more production experience"
            },
            {
                "id": "app_004",
                "company": "CloudTech",
                "role": "Backend Engineer",
                "status": ApplicationStatus.SUBMITTED,
                "applied_date": (now - timedelta(days=5)).isoformat(),
                "last_update": (now - timedelta(days=5)).isoformat(),
                "match_score": 79,
                "notes": "Recently submitted"
            },
            {
                "id": "app_005",
                "company": "FinTech Co",
                "role": "Data Scientist",
                "status": ApplicationStatus.READY,
                "applied_date": None,
                "last_update": now.isoformat(),
                "match_score": 91,
                "notes": "Draft ready, not yet submitted"
            }
        ]
    
    def _generate_reminders(self) -> List[Dict]:
        """Generate reminders for follow-ups."""
        now = datetime.now()
        
        return [
            {
                "id": "rem_001",
                "type": "follow_up",
                "application_id": "app_002",
                "company": "DataFlow Inc",
                "message": "Follow up on application (10 days since submission)",
                "due_date": now.isoformat(),
                "priority": "medium",
                "completed": False
            },
            {
                "id": "rem_002",
                "type": "interview_prep",
                "application_id": "app_001",
                "company": "TechCorp",
                "message": "Prepare for technical interview in 3 days",
                "due_date": (now + timedelta(days=2)).isoformat(),
                "priority": "high",
                "completed": False
            },
            {
                "id": "rem_003",
                "type": "application",
                "application_id": "app_005",
                "company": "FinTech Co",
                "message": "Submit application to FinTech Co (high match score)",
                "due_date": (now + timedelta(days=1)).isoformat(),
                "priority": "high",
                "completed": False
            }
        ]
    
    def _count_by_status(self) -> Dict:
        """Count applications by status."""
        counts = {}
        for app in self.applications:
            status = app["status"]
            counts[status] = counts.get(status, 0) + 1
        return counts
    
    def _calculate_response_rate(self) -> float:
        """Calculate response rate."""
        submitted = len([a for a in self.applications if a["status"] != ApplicationStatus.READY])
        responded = len([a for a in self.applications if a["status"] not in [ApplicationStatus.READY, ApplicationStatus.SUBMITTED]])
        return round((responded / max(submitted, 1)) * 100, 1)
    
    def _calculate_interview_rate(self) -> float:
        """Calculate interview rate."""
        submitted = len([a for a in self.applications if a["status"] != ApplicationStatus.READY])
        interviews = len([a for a in self.applications if a["status"] == ApplicationStatus.INTERVIEW_SCHEDULED])
        return round((interviews / max(submitted, 1)) * 100, 1)


# Global workflow instance (in production, this would be per-user)
workflow = AgenticWorkflow()


def get_workflow() -> AgenticWorkflow:
    """Get the global workflow instance."""
    return workflow
