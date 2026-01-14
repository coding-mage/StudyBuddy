# backend/gemini_client.py
import os
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv
from ddgs import DDGS
import re

# Load environment variables
load_dotenv()

def format_with_sources(answer: str, web_results: List[Dict[str, str]]) -> Dict:
    """Return both plain text answer and structured source list."""
    resp =  {
        "answer": answer,
        "sources": [
            {"id": idx, "title": item["title"], "url": item["href"]}
            for idx, item in enumerate(web_results, start=1)
        ]
    }

    # Build the string
    output = f"Answer:\n\n{resp['answer'].strip()}\n\nSources:\n"
    for src in resp['sources']:
        output += f"[{src['id']}] {src['title']}\n    {src['url']}\n"
        print({src['id']}, src['title'], src['url'])
    print(output)
    return output



def sanitize_input(text: str, max_len: int = 2000) -> str:
    """Basic cleanup to avoid prompt injection or runaway prompts."""
    if not text:
        return ""
    t = text.strip()
    if len(t) > max_len:
        t = t[:max_len]
    # remove angle brackets to avoid HTML-style injections
    t = re.sub(r"[<>]", "", t)
    return t


# function uses a query string and duckduckgo_search library to perform a web search
def perform_web_search(query: str, max_results: int = 6) -> List[Dict[str, str]]:
    """Perform a DuckDuckGo search and return a list of results.

    Each result contains: title, href, body.
    """
    results: List[Dict[str, str]] = []
    try:
        with DDGS() as ddgs:
            for result in ddgs.text(query, max_results=max_results):
                # result keys typically include: title, href, body
                if not isinstance(result, dict):
                    continue
                title = result.get('title') or ''
                href = result.get('href') or ''
                body = result.get('body') or ''
                if title and href:
                    results.append({
                        'title': title,
                        'href': href,
                        'body': body,
                    })
        print(results)
        return results
    except Exception as e:
        print(f"DuckDuckGo search error: {e}")
        return []

# A class that manages the interaction with the Gemini API and core agent logic 
class GeminiClient:
    def __init__(self):
        try:
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.chat = self.model.start_chat(history=[])
            self.history: List[Dict[str, str]] = []
        except Exception as e:
            print(f"Error configuring Gemini API: {e}")
            self.chat = None
            self.history: List[Dict[str, str]] = []

        self.modes = {
                "default": "You are a helpful AI assistant.",
                "tutor": "You are a patient teacher explaining concepts step by step.",
                "planner": "You are an academic advisor creating study plans.",
                "researcher": "You are a research assistant providing cited answers."
            }
        self.current_mode = "default"

    def set_mode(self, mode: str):
        """Switches assistant mode"""
        if mode in self.modes:
            self.current_mode = mode
            return f"Mode set to {mode}"
        return "Unknown mode."

    def add_to_history(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        # keep only last 20 messages
        self.history = self.history[-20:]

    def generate_response(self, user_input: str) -> str:
        """Generate an AI response with optional web search when prefixed.

        To trigger web search, start your message with one of:
        - "search: <query>"
        - "/search <query>"
        Otherwise, the model responds directly using chat history.
        """
        if not self.chat:
            return "AI service is not configured correctly."

        try:
            text = user_input or ""
            text = sanitize_input(user_input)
            lower = text.strip().lower()

            # Search trigger
            search_query = None
            if lower.startswith("search:"):
                search_query = text.split(":", 1)[1].strip()
            elif lower.startswith("/search "):
                search_query = text.split(" ", 1)[1].strip()
            elif lower.startswith("/clear"):
                self.chat = self.model.start_chat(history=[])
                return "Chat history cleared"

            elif lower.startswith("/summary"):
                return self.chat.send_message("Summarize our conversation so far.").text

            elif lower.startswith("/plan"):
                return self.chat.send_message(
                    "Create a 1-week study plan for the user’s last question, with daily goals."
                ).text
            elif lower.startswith("/mode "):
                mode = lower.split(" ", 1)[1]
                return self.set_mode(mode)
            
            elif lower.startswith("/help"):
                return (
                    "Available commands:\n"
                    "/search <query> → web search + answer\n"
                    "/clear → reset chat\n"
                    "/summary → summarize chat\n"
                    "/plan → create 1-week study plan\n"
                    "/mode <default|tutor|planner|researcher> → switch style"
                )

            if search_query:
                web_results = perform_web_search(search_query, max_results=6)
            if not web_results:
                return "I could not retrieve web results right now. Please try again."

            # Build context with numbered references
            refs_lines = []
            for idx, item in enumerate(web_results, start=1):
                refs_lines.append(f"[{idx}] {item['title']} — {item['href']}\n{item['body']}")
            refs_block = "\n\n".join(refs_lines)
            print(refs_block)

            system_prompt = (
                "You are an AI research assistant. Use the provided web search results to answer the user query. "
                "Synthesize concisely, cite sources inline like [1], [2] where relevant, and include a brief summary."
            )

            # ✅ Compose a proper message for Gemini
            composed = (
                f"<system>\n{system_prompt}\n</system>\n"
                f"<user_query>\n{search_query}\n</user_query>\n"
                f"<web_results>\n{refs_block}\n</web_results>"
            )

            response = self.chat.send_message(composed)
            answer_text = response.text if hasattr(response, "text") else str(response)

            print("************")
            print(answer_text)

            self.add_to_history("user", search_query)
            self.add_to_history("ai", answer_text)

            return format_with_sources(answer_text, web_results)

        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I encountered an error processing your request."