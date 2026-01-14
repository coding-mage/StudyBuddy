# backend/agents/translator.py
from transformers import pipeline

class TranslationAgent:
    def __init__(self, llm):
        self.llm = llm
        self.translator = None  # lazy-loaded fallback

    def _load_model(self):
        if self.translator is None:
            self.translator = pipeline(
                "translation",
                model="facebook/nllb-200-distilled-600M"
            )

    def run(self, payload):
        text = payload["text"]
        target = payload.get("target", "English")

        # OPTION A (recommended): Use LLM for flexible translation
        prompt = f"""
Translate the following text into {target}.
Preserve meaning and structure.

Text:
{text}
"""
        translated = self.llm.generate(prompt)

        return {
            "type": "translation",
            "content": translated.strip()
        }
