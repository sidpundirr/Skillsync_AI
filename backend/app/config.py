"""Application configuration and environment loading."""

from pathlib import Path

from dotenv import load_dotenv


load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")


class Settings:
    """Provides validated application settings sourced from environment variables."""

    def __init__(self) -> None:
        self.groq_api_key = self._get_required_env("GROQ_API_KEY")

    @staticmethod
    def _get_required_env(name: str) -> str:
        """Return a required environment variable or raise a clear error."""

        from os import getenv

        value = getenv(name)
        if not value:
            raise ValueError(
                f"Missing required environment variable: {name}. "
                "Define it in the environment or in the project's .env file."
            )

        return value


settings = Settings()
