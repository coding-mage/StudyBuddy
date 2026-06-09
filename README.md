# StudyBuddy

StudyBuddy is a multi-agent AI learning system designed to support guided learning, revision, translation, and exam preparation. It features pedagogical agents, multi-modal capabilities, and an API-first architecture, powered by local open-source models with no vendor lock-in.

## Features & Learning Modes

Each learning mode is managed by a dedicated agent orchestrated through a central router:

1. **Default Mode**: General explanation engine providing direct, clear answers to questions.
2. **Socratic Tutor Mode**: Guided reasoning that asks leading questions to prompt the learner to arrive at the answer independently.
3. **Analogy Mode**: Metaphorical explanations matching complex concepts to everyday analogies.
4. **Examiner Mode**: Generates mock exam questions, model answers, and constructive feedback for exam and interview preparation.
5. **General Translation Mode**: Meaning-preserving translation of academic texts across multiple languages.
6. **Audio Summary Mode**: Generates a podcast-style summary and converts it to audio via text-to-speech.

## Context Preservation

The frontend stores conversation history and transmits it with each request. The central orchestrator provides context to the downstream agents to enable coherent, multi-turn follow-ups, which is essential for guided Socratic tutor dialogues.

## Architecture

```
            +---------------------------+
            |      UI (HTML + CSS)      |
            +-------------+-------------+
                          | HTTP
                          v
            +---------------------------+
            |     Flask API Router      |
            +-------------+-------------+
                          |
                          v
            +---------------------------+
            |   Learning Orchestrator   |
            +-------------+-------------+
                          |
             +------------+------------+
             |                         |
             v                         v
     +-------+--------+        +-------+--------+
     | Default Agent  |        | Socratic Agent | ...
     +-------+--------+        +-------+--------+
             |                         |
             +------------+------------+
                          |
                          v
            +---------------------------+
            |    Local LLM (Ollama)     |
            +---------------------------+
```

## Technical Stack

- **Backend**: Python, Flask
- **LLM Runtime**: Ollama (configured for Llama 3)
- **Frontend**: HTML, TailwindCSS, Vanilla JavaScript
- **Audio Synthesis**: Coqui TTS
- **OCR (Optional)**: Tesseract
- **Vector Search (Optional)**: FAISS

## Getting Started

### 1. Configure local LLM runtime (Ollama)
Install and run Ollama with Llama 3:
```bash
brew install ollama
ollama serve
ollama run llama3
```

### 2. Configure Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
   The API will bind to `http://127.0.0.1:5050` by default.

### 3. Open UI
Access the application by navigating to `http://127.0.0.1:5050` in a web browser.
