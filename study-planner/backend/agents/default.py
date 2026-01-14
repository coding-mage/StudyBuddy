from agents.base import BaseAgent

class DefaultAgent(BaseAgent):
    def run(self, payload):
        prompt = f"""
You are a helpful study assistant.
Answer clearly.

Question:
{payload["message"]}
"""
        return {
            "type": "answer",
            "content": self.llm.generate(prompt)
        }
