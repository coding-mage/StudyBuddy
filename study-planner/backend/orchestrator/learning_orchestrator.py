class LearningOrchestrator:
    def __init__(self, agents):
        self.agents = agents

    def handle(self, intent, payload):
        agent = self.agents.get(intent)
        if not agent:
            return {"type": "error", "content": "Unknown intent"}
        return agent.run(payload)
