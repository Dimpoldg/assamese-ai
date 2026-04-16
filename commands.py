"""
commands.py — Custom command handler for Assamese AI
Add new commands here without touching main.py
"""

from datetime import datetime
from typing import Optional, Dict

# ─── Command Registry ────────────────────────────────────────────────────────
# Each command: list of trigger phrases → action + response
COMMAND_REGISTRY = [

    # ── Website Openers ──────────────────────────────────────────────────────
    {
        "triggers": ["open youtube", "youtube kholo", "youtube open karo", "youtube chalao"],
        "action":   "open_url",
        "url":      "https://youtube.com",
        "response": "YouTube khol raha hun! 🎬"
    },
    {
        "triggers": ["open google", "google kholo", "google open"],
        "action":   "open_url",
        "url":      "https://google.com",
        "response": "Google khol raha hun! 🔍"
    },
    {
        "triggers": ["open whatsapp", "whatsapp kholo", "whatsapp open"],
        "action":   "open_url",
        "url":      "https://web.whatsapp.com",
        "response": "WhatsApp Web khol raha hun! 💬"
    },
    {
        "triggers": ["open instagram", "instagram kholo", "insta kholo"],
        "action":   "open_url",
        "url":      "https://instagram.com",
        "response": "Instagram khol raha hun! 📸"
    },
    {
        "triggers": ["open facebook", "facebook kholo", "fb kholo"],
        "action":   "open_url",
        "url":      "https://facebook.com",
        "response": "Facebook khol raha hun! 📘"
    },
    {
        "triggers": ["open twitter", "twitter kholo", "x kholo"],
        "action":   "open_url",
        "url":      "https://twitter.com",
        "response": "Twitter / X khol raha hun! 🐦"
    },
    {
        "triggers": ["open gmail", "gmail kholo", "email kholo"],
        "action":   "open_url",
        "url":      "https://mail.google.com",
        "response": "Gmail khol raha hun! 📧"
    },
    {
        "triggers": ["open maps", "maps kholo", "location dekho"],
        "action":   "open_url",
        "url":      "https://maps.google.com",
        "response": "Google Maps khol raha hun! 🗺️"
    },
    {
        "triggers": ["open spotify", "spotify kholo", "music chalao"],
        "action":   "open_url",
        "url":      "https://open.spotify.com",
        "response": "Spotify khol raha hun! 🎵"
    },
    {
        "triggers": ["open netflix", "netflix kholo"],
        "action":   "open_url",
        "url":      "https://netflix.com",
        "response": "Netflix khol raha hun! 🎬"
    },
    {
        "triggers": ["open amazon", "amazon kholo", "shopping kholo"],
        "action":   "open_url",
        "url":      "https://amazon.in",
        "response": "Amazon India khol raha hun! 🛍️"
    },
    {
        "triggers": ["open github", "github kholo"],
        "action":   "open_url",
        "url":      "https://github.com",
        "response": "GitHub khol raha hun! 💻"
    },

    # ── System Commands ──────────────────────────────────────────────────────
    {
        "triggers": ["time kya hai", "abhi ka time", "what time is it", "time batao"],
        "action":   "get_time",
        "response": None  # Generated dynamically
    },
    {
        "triggers": ["aaj ki date", "today's date", "date kya hai", "date batao"],
        "action":   "get_date",
        "response": None
    },
    {
        "triggers": ["help", "kya kar sakte ho", "features batao", "commands batao"],
        "action":   "help",
        "response": None
    },
]

HELP_TEXT = """🤖 **Assamese AI — Available Commands**

🌐 **Website Commands:**
• "Open YouTube / YouTube kholo"
• "Open Google / Google kholo"
• "Open WhatsApp / WhatsApp kholo"
• "Open Instagram / Insta kholo"
• "Open Gmail / Gmail kholo"
• "Open Maps / Maps kholo"
• "Open Spotify / Spotify kholo"
• "Open Netflix / Netflix kholo"
• "Open Amazon / Amazon kholo"
• "Open GitHub / GitHub kholo"

🕐 **System Commands:**
• "Time kya hai" — current time
• "Aaj ki date" — today's date

💬 **AI Commands:**
• Any question in Hindi, English, or Assamese
• "Mausam kaisa hai?" — weather
• "Latest news kya hai?" — news
• "Python code likhdo" — coding help

🎙️ **Voice:**
• Mic button se bolkar poochh sakte hain
• 🔊 button se jawab sunn sakte hain
"""


def handle_command(message: str) -> Optional[Dict]:
    """
    Match message against command registry.
    Returns dict with response/action if matched, else None.
    """
    msg_lower = message.lower().strip()

    for cmd in COMMAND_REGISTRY:
        if any(trigger in msg_lower for trigger in cmd["triggers"]):

            if cmd["action"] == "get_time":
                now = datetime.now()
                time_str = now.strftime("%I:%M %p")
                return {
                    "response": f"🕐 Abhi ka time hai: **{time_str}**",
                    "action": "none"
                }

            elif cmd["action"] == "get_date":
                now = datetime.now()
                date_str = now.strftime("%A, %d %B %Y")
                return {
                    "response": f"📅 Aaj ki date: **{date_str}**",
                    "action": "none"
                }

            elif cmd["action"] == "help":
                return {
                    "response": HELP_TEXT,
                    "action": "none"
                }

            else:
                return {
                    "response": cmd["response"],
                    "action":   cmd["action"],
                    "url":      cmd.get("url")
                }

    return None


# ─── Easy way to add custom commands ─────────────────────────────────────────
def add_command(triggers: list, action: str, response: str, url: str = None):
    """
    Dynamically add new commands at runtime.
    Example:
        add_command(["open paytm", "paytm kholo"], "open_url",
                    "Paytm khol raha hun!", "https://paytm.com")
    """
    COMMAND_REGISTRY.append({
        "triggers": [t.lower() for t in triggers],
        "action":   action,
        "url":      url,
        "response": response
    })
