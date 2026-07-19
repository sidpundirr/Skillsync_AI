"""Shared state definitions for the LangGraph career analysis workflow."""

from typing import TypedDict


class CareerState(TypedDict):
    """Represents the shared LangGraph state passed between workflow nodes."""

    resume_text: str
    job_description: str
    resume_data: dict
    job_data: dict
    matched_skills: list[str]
    missing_skills: list[str]
    match_score: int
    roadmap: str
    courses: list[str]
    report: str
