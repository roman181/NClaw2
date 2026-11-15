from backend.agents.nexus import NexusAgent


class AgentRegistry:
    def __init__(self) -> None:
        self._agents = {"nexus": NexusAgent()}

    def list(self) -> list[dict[str, str]]:
        return [
            {"id": agent.agent_id, "name": agent.name, "role": agent.role, "status": "online"}
            for agent in self._agents.values()
        ]

    def get(self, agent_id: str):
        return self._agents.get(agent_id)


registry = AgentRegistry()
