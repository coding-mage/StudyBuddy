from agents.base import BaseAgent

class ElaborativeAgent(BaseAgent):
    def run(self, payload):
        prompt = f"""
Explain "{payload["concept"]}"
using an analogy related to "{payload.get("hobby", "daily life")}".
"""
        return {
            "type": "analogy",
            "content": self.llm.generate(prompt)
        }
