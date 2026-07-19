"""Skill matching node for populating match results in shared state."""

from app.agents.state import CareerState
from app.services.skill_matcher import SkillMatcher


class SkillMatcherNode:
    """Matches extracted resume and job skills using the existing skill matcher service."""

    def __init__(self, skill_matcher: SkillMatcher | None = None) -> None:
        self._skill_matcher = skill_matcher or SkillMatcher()

    def run(self, state: CareerState) -> CareerState:
        """Return updated state with skill match results populated."""

        resume_skills = state["resume_data"].get("skills", [])
        job_skills = state["job_data"].get("skills", [])
        match_result = self._skill_matcher.match(resume_skills, job_skills)

        updated_state = dict(state)
        updated_state["match_score"] = match_result["match_score"]
        updated_state["matched_skills"] = match_result["matched_skills"]
        updated_state["missing_skills"] = match_result["missing_skills"]
        return updated_state
