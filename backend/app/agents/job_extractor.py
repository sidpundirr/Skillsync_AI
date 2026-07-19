"""Job description extraction node for populating structured job data in shared state."""

import json

from app.agents.state import CareerState
from app.services.groq_service import GroqService


class JobExtractor:
    """Extracts technical skills from a job description using the Groq service."""

    def __init__(self, groq_service: GroqService | None = None) -> None:
        self._groq_service = groq_service or GroqService()

    def run(self, state: CareerState) -> CareerState:
        """Return updated state with extracted job skills in `job_data`."""

        response = self._groq_service.generate(self._build_prompt(state["job_description"]))
        parsed_skills = self._parse_response(response)

        updated_state = dict(state)
        updated_state["job_data"] = {"skills": parsed_skills}
        return updated_state

    @staticmethod
    def _build_prompt(job_description: str) -> str:
        """Build a prompt that requests JSON-only skill extraction."""

        return (
            "Extract only the technical skills from the job description below.\n"
            "Return JSON only in this exact format:\n"
            '{"skills": ["skill 1", "skill 2"]}\n'
            "Do not include markdown, explanations, or any text outside the JSON object.\n\n"
            f"Job description:\n{job_description}"
        )

    @staticmethod
    def _parse_response(response: str) -> list[str]:
        """Safely parse the model response and return a sanitized skills list."""

        try:
            payload = json.loads(response)
        except json.JSONDecodeError:
            return []

        if not isinstance(payload, dict):
            return []

        skills = payload.get("skills", [])
        if not isinstance(skills, list):
            return []

        cleaned_skills: list[str] = []
        for skill in skills:
            if not isinstance(skill, str):
                continue

            cleaned_skill = skill.strip()
            if cleaned_skill:
                cleaned_skills.append(cleaned_skill)

        return cleaned_skills
