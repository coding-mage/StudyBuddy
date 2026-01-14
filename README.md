📘 StudyBuddy – An Open-Source, Multi-Agent AI Learning OS

StudyBuddy is an open-source, multi-agent AI learning system designed to go beyond a simple chatbot or summarizer.
It combines pedagogical agents, multi-modal capabilities, and a clean API-first architecture to support deep learning, revision, and exam preparation.

The project is built with OSS technologies only and runs locally, with no vendor lock-in.

✨ Key Highlights

🤖 Multi-Agent Architecture (not a single chatbot)

🧠 Pedagogy-driven learning modes

🎧 Audio (podcast-style) explanations

🌍 General-purpose translation

🧩 Context-aware conversations

🔓 Fully open-source stack

🧠 Learning Modes (Agents)

Each mode is implemented as a separate agent, orchestrated through a central router.

1. Default Mode

Purpose: Direct explanations
Ask any question and receive a clear, concise answer.

Best for:
Quick understanding
Revision
Fact checking

2. Socratic Tutor Mode

Purpose: Guided thinking instead of direct answers
The agent responds with carefully chosen questions that help the learner arrive at the answer step by step.

Why it matters:
This mode is based on Socratic pedagogy, encouraging deeper understanding rather than memorization.

3. Explain with Analogy Mode

Purpose: Improve retention using analogies
Complex concepts are explained using everyday metaphors or user-provided contexts (e.g. cooking, music, puzzles).


4. Examiner Mode

Purpose: Self-assessment and interview preparation
Generates mock exam questions, model answers, and feedback.

Best for:
Interview prep
Concept validation
Exam revision

5. Translation Mode (General-Purpose)

Purpose: Translate learning material between languages
Supports any source → any target language, preserving meaning and structure.

Use cases:

Studying from foreign textbooks
Understanding technical material in another language
Language-assisted learning

6. Audio Summary Mode

Purpose: Learn by listening
Generates a podcast-style spoken explanation, then converts it to audio using TTS.

Best for:
Revision while commuting
Passive learning
Accessibility

🧩 Context Preservation

StudyBuddy supports context-aware conversations.
Conversation history is preserved on the frontend
History is sent with each request
Agents use recent turns to generate coherent follow-ups

This ensures:
Socratic conversations don’t derail
Follow-up answers remain relevant
Learning feels continuous

🏗️ Architecture Overview

UI (HTML + Tailwind)
   ↓
Flask API (/api/chat)
   ↓
Learning Orchestrator
   ↓
Specialized Agents
   ├── Default Agent
   ├── Socratic Agent
   ├── Elaborative Agent
   ├── Examiner Agent
   ├── Translation Agent
   └── Audio Summary Agent
   ↓
LLM Runtime (Ollama)


🧰 Technology Stack

Backend: Python, Flask
LLM Runtime: Ollama (local models like LLaMA 3)
Frontend: HTML, TailwindCSS, Vanilla JavaScript
Audio: Coqui TTS
Translation: LLM-based (generalized)
OCR (optional): Tesseract
Vector Search (future): FAISS
