from langchain.tools import tool
import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def get_secret(name: str) -> str | None:
    value = os.getenv(name)
    if value:
        return value
    try:
        import streamlit as st

        return st.secrets.get(name)
    except Exception:
        return None


tavily_api_key = get_secret("TAVILY_API_KEY")
tavily = TavilyClient(api_key=tavily_api_key) if tavily_api_key else None


def search_web(query: str) -> str:
    """Plain Python helper for direct calls and local validation."""
    if tavily is None:
        return "TAVILY_API_KEY is not configured. Set it in the environment or Streamlit secrets to enable web search."

    try:
        results = tavily.search(query=query, max_results=5)
        return "\n----\n".join(
            f"Title: {result['title']}\n"
            f"URL: {result['url']}\n"
            f"Snippet: {result['content'][:300]}\n"
            for result in results.get("results", [])
        )
    except Exception as error:
        return f"Web search failed: {error}"


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic."""
    return search_web(query)


def scrape_url_page(url: str) -> str:
    """Plain Python helper for direct scrapes and local validation."""
    try:
        response = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except requests.RequestException as error:
        return f"Could not scrape URL: {error}"


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a URL."""
    return scrape_url_page(url)
