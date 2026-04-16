"""
Assamese AI — Backend API
FastAPI + SQLite + Anthropic + DuckDuckGo Search
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

from database import init_db, save_message, get_history, clear_history
from commands import handle_command
from search import web_search

load_dotenv()

# ─── App Setup ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="Assamese AI API",
    description="Backend for Assamese AI personal assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── AI Client ────────────────────────────────────────────────────────────────
import anthropic
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are Assamese AI — a smart, friendly, and multilingual personal assistant.
You support Hindi, English, and Assamese languages.
Always detect the language the user writes in and reply in the SAME language.
If the user writes in Hindi → reply in Hindi.
If the user writes in English → reply in English.
If the user writes in Assamese → reply in Assamese or Hindi.

Your personality:
- Warm, helpful, and concise
- You know general knowledge, coding, health, news, and daily tasks
- You execute custom commands like opening websites
- You NEVER mention ChatGPT, Claude, Gemini, or any AI brand
- You ARE Assamese AI — an independent, original product

When answering questions that need real-time info (weather, news, stock prices),
the context will include web search results — use them to give accurate answers.
"""

# ─── Models ──────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    language: Optional[str] = "auto"

class ChatResponse(BaseModel):
    response: str
    type: str = "text"
    action: Optional[str] = None
    url: Optional[str] = None

# ─── Events ──────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    init_db()
    print("✅ Assamese AI backend started!")
    print(f"✅ API Key loaded: {'YES' if os.getenv('ANTHROPIC_API_KEY') else 'NO — set ANTHROPIC_API_KEY in .env'}")

# ─── Routes ──────────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"message": "Assamese AI is running! 🚀", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "ok", "assistant": "Assamese AI", "version": "1.0.0"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Main chat endpoint — processes message and returns AI response"""

    # 1. Handle custom commands first (instant, no AI call needed)
    cmd_result = handle_command(req.message)
    if cmd_result:
        save_message(req.session_id, "user", req.message)
        save_message(req.session_id, "assistant", cmd_result["response"])
        return ChatResponse(
            response=cmd_result["response"],
            type="command",
            action=cmd_result.get("action"),
            url=cmd_result.get("url")
        )

    # 2. Check if web search is needed
    search_context = ""
    search_triggers = [
        "weather", "mausam", "news", "khabar", "latest", "aaj ka",
        "today", "current", "abhi", "price", "kimat", "score",
        "result", "nataija", "stock", "rate"
    ]
    if any(t in req.message.lower() for t in search_triggers):
        results = web_search(req.message)
        if results:
            search_context = f"\n\n[Web Search Results for context]\n{results}\n[End of search results]\n"

    # 3. Build message history with search context
    history = get_history(req.session_id, limit=12)
    user_content = req.message + (search_context if search_context else "")
    messages = history + [{"role": "user", "content": user_content}]

    # 4. Call AI
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=messages
        )
        reply = response.content[0].text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")

    # 5. Save to memory
    save_message(req.session_id, "user", req.message)
    save_message(req.session_id, "assistant", reply)

    return ChatResponse(response=reply, type="text")


@app.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    """Retrieve conversation history for a session"""
    return {"session_id": session_id, "history": get_history(session_id, limit=50)}


@app.delete("/history/{session_id}")
async def clear_chat_history(session_id: str):
    """Clear conversation history for a session"""
    clear_history(session_id)
    return {"message": "History cleared successfully", "session_id": session_id}


@app.get("/sessions")
async def list_sessions():
    """List all active sessions (admin use)"""
    from database import list_sessions as ls
    return {"sessions": ls()}
