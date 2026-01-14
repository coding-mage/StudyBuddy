# backend/agents/audio_summary.py
from TTS.api import TTS

class AudioSummaryAgent:
    def __init__(self, llm):
        self.llm = llm
        self.tts = None  # lazy load

    def _load_tts(self):
        if self.tts is None:
            self.tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")

    def run(self, payload):
        topic = payload["text"]

        # 1️⃣ Generate spoken-style script using LLM
        prompt = f"""
Create a short podcast-style explanation (2–3 minutes)
about the following topic.

Rules:
- Conversational tone
- No bullet points
- Explain like you're talking to a learner
- Do NOT repeat the question

Topic:
{topic}
"""

        script = self.llm.generate(prompt)

        # 2️⃣ Convert script to audio
        self._load_tts()
        output_path = "summary.wav"
        self.tts.tts_to_file(
            text=script,
            file_path=output_path
        )

        return {
            "type": "audio",
            "file": output_path,
            "script": script  # optional, useful for debugging/UI
        }
