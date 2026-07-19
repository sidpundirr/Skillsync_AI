"""Career advisory node for generating guidance from match analysis state."""

import json

from app.agents.state import CareerState
from app.services.groq_service import GroqService


class CareerAdvisor:
    """Generates a roadmap, courses, and report from skill match results."""

    def __init__(self, groq_service: GroqService | None = None) -> None:
        self._groq_service = groq_service or GroqService()

    def run(self, state: CareerState) -> CareerState:
        """Return updated state with career guidance fields populated."""

        response = self._groq_service.generate(
            self._build_prompt(
                state["match_score"],
                state["matched_skills"],
                state["missing_skills"],
            )
        )
        parsed_response = self._parse_response(response)

        updated_state = dict(state)
        updated_state["roadmap"] = parsed_response["roadmap"]
        updated_state["courses"] = parsed_response["courses"]
        updated_state["report"] = parsed_response["report"]
        return updated_state

    @staticmethod
    def _build_prompt(
        match_score: int,
        matched_skills: list[str],
        missing_skills: list[str],
    ) -> str:
        """Build a prompt that requests JSON-only career guidance output."""

        return (
            "You are a career advisor helping a candidate improve job readiness.\n"
            "Based on the match analysis below, return JSON only in this exact format:\n"
            '{\n'
            '  "roadmap": "string",\n'
            '  "courses": [\n'
            '    "course 1",\n'
            '    "course 2",\n'
            '    "course 3"\n'
            "  ],\n"
            '  "report": "string"\n'
            "}\n"
            "Do not include markdown, explanations, or any text outside the JSON object.\n\n"
            f"Match score: {match_score}\n"
            f"Matched skills: {matched_skills}\n"
            f"Missing skills: {missing_skills}"
        )

    @staticmethod
    def _parse_response(response: str) -> dict[str, str | list[str]]:
        """Safely parse the model response and return advisory content."""

        empty_response: dict[str, str | list[str]] = {
            "roadmap": "",
            "courses": [],
            "report": "",
        }

        try:
            payload = json.loads(response)
        except json.JSONDecodeError:
            return empty_response

        if not isinstance(payload, dict):
            return empty_response

        roadmap = payload.get("roadmap", "")
        courses = payload.get("courses", [])
        report = payload.get("report", "")

        if not isinstance(roadmap, str) or not isinstance(courses, list) or not isinstance(report, str):
            return empty_response

        cleaned_courses: list[str] = []
        for course in courses:
            if not isinstance(course, str):
                continue

            cleaned_course = course.strip()
            if cleaned_course:
                cleaned_courses.append(cleaned_course)

        return {
            "roadmap": roadmap.strip(),
            "courses": cleaned_courses,
            "report": report.strip(),
        }
