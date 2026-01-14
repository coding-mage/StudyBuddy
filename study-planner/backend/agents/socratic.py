from agents.base import BaseAgent

class SocraticAgent(BaseAgent):
    def run(self, payload):
       history = payload.get("history", [])

       history_text = "\n".join(
            f"{h['role'].upper()}: {h['content']}" for h in history[-6:]
        )

       prompt = f"""
        You are a Socratic tutor guiding a learner step by step.
        You MUST build on the prior conversation.

        Conversation so far:
        {history_text}

        Current topic:
        {payload["topic"]}

        Ask the next helpful guiding question.
        """

       return {
            "type": "socratic_questions",
            "content": self.llm.generate(prompt)
        }
