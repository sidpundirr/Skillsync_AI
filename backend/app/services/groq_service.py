"""Service wrapper for interacting with the Groq-hosted chat model."""

from langchain_groq import ChatGroq

from app.config import settings


class GroqService:
    """Provides a simple interface for generating text with Groq."""

    def __init__(self) -> None:
        self._llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=settings.groq_api_key,
        )

    def generate(self, prompt: str) -> str:
        """Generate a text response for the provided prompt."""

        response = self._llm.invoke(prompt)
        return response.content if isinstance(response.content, str) else str(response.content)
