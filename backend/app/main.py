from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agents.career_graph import CareerGraph
from app.schemas.career import CareerRequest, CareerResponse
from app.agents.state import CareerState

app = FastAPI(
    title="SkillSync AI API",
    description="AI-powered Career Analysis and Skill Gap Recommendation System"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = CareerGraph()


@app.get("/")
def root():
    return {"message": "Welcome to SkillSync AI API"}


@app.post("/api/v1/analyze", response_model=CareerResponse)
def analyze_career(request: CareerRequest) -> CareerResponse:
    """Analyze resume against job description and return skill match and recommendations."""
    initial_state: CareerState = {
        "resume_text": request.resume_text,
        "job_description": request.job_description,
        "resume_data": {},
        "job_data": {},
        "matched_skills": [],
        "missing_skills": [],
        "match_score": 0,
        "roadmap": "",
        "courses": [],
        "report": ""
    }
    
    final_state = graph.run(initial_state)
    
    return CareerResponse(
        match_score=final_state["match_score"],
        matched_skills=final_state["matched_skills"],
        missing_skills=final_state["missing_skills"],
        roadmap=final_state["roadmap"],
        courses=final_state["courses"],
        report=final_state["report"]
    )