"""Skill matching utilities for resume and job requirement comparisons."""

from typing import Any


class SkillMatcher:
    """Matches resume skills against job skills and calculates a match score."""

    @staticmethod
    def _normalize_skills(skills: list[str]) -> dict[str, str]:
        """Normalize skill names for case-insensitive matching while preserving display text."""

        normalized: dict[str, str] = {}
        for skill in skills:
            cleaned_skill = skill.strip()
            if not cleaned_skill:
                continue

            key = cleaned_skill.casefold()
            normalized.setdefault(key, cleaned_skill)

        return normalized

    def match(self, resume_skills: list[str], job_skills: list[str]) -> dict[str, Any]:
        """Compare resume and job skills and return a scored matching summary."""

        normalized_resume_skills = self._normalize_skills(resume_skills)
        normalized_job_skills = self._normalize_skills(job_skills)

        if not normalized_job_skills:
            return {
                "match_score": 0,
                "matched_skills": [],
                "missing_skills": [],
            }

        matched_keys = set(normalized_resume_skills) & set(normalized_job_skills)
        missing_keys = set(normalized_job_skills) - set(normalized_resume_skills)

        matched_skills = sorted(normalized_job_skills[key] for key in matched_keys)
        missing_skills = sorted(normalized_job_skills[key] for key in missing_keys)
        match_score = int((len(matched_keys) / len(normalized_job_skills)) * 100)

        return {
            "match_score": match_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
        }
