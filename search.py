"""
search.py — Web search integration for Assamese AI
Uses DuckDuckGo (free, no API key needed)
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from typing import Optional


def web_search(query: str, max_results: int = 4) -> Optional[str]:
    """
    Search the web using DuckDuckGo HTML (no API key required).
    Returns formatted string with search results, or None on failure.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }

        url = f"https://html.duckduckgo.com/html/?q={quote(query)}&kl=in-en"
        response = requests.get(url, headers=headers, timeout=6)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for item in soup.select(".result")[:max_results]:
            title_el   = item.select_one(".result__title")
            snippet_el = item.select_one(".result__snippet")
            url_el     = item.select_one(".result__url")

            if title_el and snippet_el:
                title   = title_el.get_text(strip=True)
                snippet = snippet_el.get_text(strip=True)
                source  = url_el.get_text(strip=True) if url_el else ""
                results.append(f"• {title}\n  {snippet}\n  Source: {source}")

        if results:
            return "\n\n".join(results)

        return None

    except requests.exceptions.Timeout:
        print("⚠️ Web search timeout")
        return None
    except Exception as e:
        print(f"⚠️ Web search error: {e}")
        return None


def search_news(query: str) -> Optional[str]:
    """Search for latest news on a topic"""
    return web_search(f"{query} latest news 2024", max_results=3)


def search_weather(location: str) -> Optional[str]:
    """Search for weather information"""
    return web_search(f"weather in {location} today", max_results=2)
