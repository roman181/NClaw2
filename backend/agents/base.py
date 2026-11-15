from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    agent_id: str
    name: str
    role: str

    @abstractmethod
    async def handle(self, task: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Handle a task and return a structured result."""
