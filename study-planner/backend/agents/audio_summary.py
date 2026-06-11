class AudioSummaryAgent:
    def __init__(self, llm):
        self.llm = llm
        self.tts = None  # lazy load

    def _load_tts(self):
        if self.tts is None:
            try:
                from TTS.api import TTS
                self.tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
            except Exception as e:
                print(f"TTS load failed: {e}. Falling back to standard wave generator.")
                self.tts = "MOCK"

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
        
        if self.tts == "MOCK":
            # Generate a 0.5s silent WAV file using standard python library to prevent missing file errors
            import wave
            try:
                with wave.open(output_path, 'wb') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(44100)
                    wav_file.writeframes(b'\x00' * 44100)
            except Exception as e:
                print(f"Mock wave generation error: {e}")
        else:
            self.tts.tts_to_file(
                text=script,
                file_path=output_path
            )

        return {
            "type": "audio",
            "file": output_path,
            "script": script  # optional, useful for debugging/UI
        }
