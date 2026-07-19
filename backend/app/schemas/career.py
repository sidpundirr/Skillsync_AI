from pydantic import BaseModel, Field


class CareerRequest(BaseModel):
    resume_text: str = Field(
        ...,
        description="The full text content extracted from the user's resume.",
    )
    job_description: str = Field(
        ...,
        description="The target job description used to evaluate candidate alignment.",
    )


class CareerResponse(BaseModel):
    match_score: float = Field(
        ...,
        description="The overall resume-to-job match score expressed as a percentage or rating.",
    )
    matched_skills: list[str] = Field(
        ...,
        description="Skills identified in both the resume and the target job description.",
    )
    missing_skills: list[str] = Field(
        ...,
        description="Relevant job skills that appear to be absent from the resume.",
    )
    roadmap: str = Field(
        ...,
        description="A personalized improvement roadmap for closing skill or experience gaps.",
    )
    courses: list[str] = Field(
        ...,
        description="Recommended courses or learning resources tailored to the candidate's gaps.",
    )
    report: str = Field(
        ...,
        description="A detailed narrative report summarizing the assessment and recommendations.",
    )
