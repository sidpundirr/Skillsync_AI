"""Minimal script for verifying GroqService connectivity."""

from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.services.groq_service import GroqService


def main() -> None:
    """Instantiate the Groq service, send a test prompt, and print the response."""

    service = GroqService()
    response = service.generate("Say hello in exactly one sentence.")
    print(response)


if __name__ == "__main__":
    main()
