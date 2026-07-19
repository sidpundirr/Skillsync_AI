"""LangGraph workflow for the career analysis pipeline."""

from langgraph.graph import END, START, StateGraph

from app.agents.career_advisor import CareerAdvisor
from app.agents.job_extractor import JobExtractor
from app.agents.resume_extractor import ResumeExtractor
from app.agents.skill_matcher_node import SkillMatcherNode
from app.agents.state import CareerState


class CareerGraph:
    """Builds and runs the LangGraph workflow for career analysis."""

    def __init__(self) -> None:
        self._resume_extractor = ResumeExtractor()
        self._job_extractor = JobExtractor()
        self._skill_matcher = SkillMatcherNode()
        self._career_advisor = CareerAdvisor()
        self._graph = self._build_graph()

    def run(self, state: CareerState) -> CareerState:
        """Run the compiled graph and return the final career analysis state."""

        return self._graph.invoke(state)

    def _build_graph(self):
        """Create and compile the career analysis graph."""

        graph = StateGraph(CareerState)

        graph.add_node("resume_extractor", self._resume_extractor.run)
        graph.add_node("job_extractor", self._job_extractor.run)
        graph.add_node("skill_matcher", self._skill_matcher.run)
        graph.add_node("career_advisor", self._career_advisor.run)

        graph.add_edge(START, "resume_extractor")
        graph.add_edge("resume_extractor", "job_extractor")
        graph.add_edge("job_extractor", "skill_matcher")
        graph.add_edge("skill_matcher", "career_advisor")
        graph.add_edge("career_advisor", END)

        return graph.compile()
