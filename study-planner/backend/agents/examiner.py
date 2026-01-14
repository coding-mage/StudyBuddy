from agents.base import BaseAgent

class ExaminerAgent(BaseAgent):
    def run(self, payload):
        prompt = f"""
Create a mock exam.

Material:
{payload["material"]}

Difficulty: {payload.get("difficulty", "medium")}

Include questions, answers, and feedback.
"""
        return {
            "type": "mock_exam",
            "content": self.llm.generate(prompt)
        }
