import ollama

class OllamaRuntime:
    def __init__(self, model="llama3"):
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response["message"]["content"]
        except Exception as e:
            print(f"Ollama error: {e}. Using mock study planner response.")
            # Return custom mock tutor responses depending on the prompt content
            p_lower = prompt.lower()
            if "translate" in p_lower:
                return "[Mock Translator] Here is the translation for your request. Learning languages takes time, but you are doing great!"
            elif "explain" in p_lower or "socratic" in p_lower:
                return "[Mock Socratic Tutor] Excellent question! Let's break this down. Think about what we are trying to solve. What do you think is the first step?"
            elif "exam" in p_lower or "quiz" in p_lower:
                return "[Mock Examiner] Here is a quiz question to test your understanding:\n\nWhat is the time complexity of searching in a balanced binary search tree?\n- A) O(N)\n- B) O(log N)\n- C) O(1)\n\nThink about the options and explain your choice."
            else:
                return "[Mock Study Partner] That's a fascinating topic! I recommend summarizing this in your notes and practicing with sample questions. Let me know how else I can help!"

