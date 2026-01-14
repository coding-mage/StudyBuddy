from flask import Flask, request, jsonify, render_template,send_from_directory
from llm.ollama_runtime import OllamaRuntime
from orchestrator.learning_orchestrator import LearningOrchestrator

from agents.default import DefaultAgent
from agents.socratic import SocraticAgent
from agents.elaborative import ElaborativeAgent
from agents.examiner import ExaminerAgent
from agents.translator import TranslationAgent
from agents.vision_notes import VisionNotesAgent
from agents.audio_summary import AudioSummaryAgent


import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates")
)

llm = OllamaRuntime()

orchestrator = LearningOrchestrator({
    "default": DefaultAgent(llm),
    "socratic": SocraticAgent(llm),
    "explain": ElaborativeAgent(llm),
    "exam": ExaminerAgent(llm),
    "translate": TranslationAgent(llm),
    "vision": VisionNotesAgent(),
    "audio": AudioSummaryAgent(llm)
})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/summary.wav")
def serve_audio():
    return send_from_directory(".", "summary.wav")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    intent = data.get("intent", "default")
    payload = data.get("payload", {})
    payload["history"] = data.get("history", [])

    response = orchestrator.handle(intent, payload)
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5050)

