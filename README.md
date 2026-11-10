# 🔬 ResearchMind | Multi-Agent AI Research System

> **An autonomous multi-agent research assistant that gathers real-time web intelligence, extracts deep primary source content, synthesizes structured reports, and performs automated self-critique.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-1C3C3C?logo=chainlink&logoColor=white)](https://www.langchain.com/)
[![OpenAI](https://img.shields.io/badge/Model-GPT--4o--mini-412991?logo=openai&logoColor=white)](https://openai.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Executive Summary (The 30-Second Pitch)

Standard LLMs struggle with recent topics, hallucinate unsourced claims, and cannot read external web pages in depth. **ResearchMind** solves this by orchestrating **four specialized AI agents and chains** into an automated research pipeline:

1. **Search Agent**: Queries the live web using Tavily API to find top authoritative sources and snippets.
2. **Reader Agent**: Autonomously inspects the results, selects the highest-signal URL, and scrapes its full article content.
3. **Writer Chain**: Synthesizes the search results and scraped content into a formal, structured research report with citations.
4. **Critic Chain**: Acts as an automated peer-reviewer (*LLM-as-a-Judge*), scoring the report out of 10 and highlighting strengths and areas to improve.

Users can interact with the system via a **Streamlit Web Dashboard** (with live progress tracking and Markdown download) or run it as a **standalone CLI pipeline**.

---

## 🏗️ System Architecture & Workflow

```text
               ┌─────────────────────────────────────────────────────┐
               │                User Input (Topic)                   │
               └──────────────────────────┬──────────────────────────┘
                                          │
                                          ▼
   ┌─────────────────────────────────────────────────────────────────────────────────┐
   │ 1. SEARCH AGENT (LangChain Tool Agent + Tavily API)                             │
   │    • Generates search query                                                     │
   │    • Retrieves top 5 recent web sources, titles, and snippets                   │
   └──────────────────────────────────────┬──────────────────────────────────────────┘
                                          │  Search Results
                                          ▼
   ┌─────────────────────────────────────────────────────────────────────────────────┐
   │ 2. READER AGENT (LangChain Tool Agent + BeautifulSoup)                          │
   │    • Evaluates search results to pick the single most relevant URL              │
   │    • Scrapes full web page text, stripping scripts, styles, and boilerplate     │
   └──────────────────────────────────────┬──────────────────────────────────────────┘
                                          │  Deep Scraped Content
                                          ▼
   ┌─────────────────────────────────────────────────────────────────────────────────┐
   │ 3. WRITER CHAIN (LangChain LCEL Prompt + GPT-4o-mini)                           │
   │    • Combines search snippets + deep scraped body content                       │
   │    • Generates structured report: Introduction, Key Findings, Conclusion, URLs  │
   └──────────────────────────────────────┬──────────────────────────────────────────┘
                                          │  Drafted Report
                                          ▼
   ┌─────────────────────────────────────────────────────────────────────────────────┐
   │ 4. CRITIC CHAIN (LangChain LCEL Evaluation Prompt + GPT-4o-mini)                │
   │    • Audits report accuracy, completeness, and structure                        │
   │    • Outputs: Score (X/10), Strengths, Areas to Improve, Final Verdict          │
   └──────────────────────────────────────┬──────────────────────────────────────────┘
                                          │
                                          ▼
               ┌─────────────────────────────────────────────────────┐
               │   Output: Streamlit Dashboard / Downloadable .md    │
               └─────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

A clean, focused codebase with zero unnecessary files:

```text
Multi-Agent-System/
├── agents.py           # Agent definitions, prompts, and LCEL chains
├── app.py              # Streamlit web application with custom dark theme
├── pipeline.py         # Standalone CLI workflow for terminal execution
├── tools.py            # Tavily web search tool and BeautifulSoup web scraper
├── requirements.txt    # Minimal, clean project dependencies
├── .env.example        # Template for required API keys
├── .gitignore          # Production Python gitignore
├── LICENSE             # MIT Open Source License
└── README.md           # Architecture, setup guide, and interview walkthrough
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/itendra-kumar-dev/Multi-Agent-System.git
cd Multi-Agent-System
```

### 2. Create and Activate Virtual Environment
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory (refer to `.env.example`):
```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```
- **OpenAI Key**: [Get API Key](https://platform.openai.com/api-keys)
- **Tavily Key**: [Get Free Search Key](https://tavily.com/)

---

## 💻 How to Run

### Option A: Interactive Web UI (Streamlit)
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser. Enter any topic (e.g., *"Quantum Computing Breakthroughs in 2025"*), run the pipeline, watch real-time step cards update, inspect raw search/scrape results, and download the report as a `.md` file.

### Option B: Terminal CLI Mode
```bash
python pipeline.py
```
Type your topic in the prompt. The terminal will log each step and print the final report alongside the critic's scorecard.

---

## 🎯 Interview Deep-Dive: Key Talking Points

When presenting this project in a machine learning / AI engineer interview, here are the architectural design decisions to emphasize:

### 1. Why a Multi-Agent System Instead of a Single Prompt?
- **Separation of Concerns**: In a single prompt, asking an LLM to search, scrape, synthesize, and review causes cognitive overload and instruction-following decay. Dividing the task allows each agent to focus on one objective.
- **Cost & Token Efficiency**: Instead of blindly scraping all 5 search results (which exhausts context windows and risks token bloat), the **Reader Agent** acts as an intelligent filter, selecting only the highest-relevance URL to scrape deeply.

### 2. How is Hallucination Mitigated?
- **Source Grounding**: The Writer Chain does not generate from memory; it is strictly constrained to the aggregated context provided by Tavily snippets and the cleaned text extracted by BeautifulSoup.
- **Citation Verification**: Every generated report must conclude with the explicit source URLs retrieved during the workflow.

### 3. Why Include a Critic Chain (LLM-as-a-Judge)?
- In production agentic systems, self-reflection and validation are critical. The Critic Chain evaluates the output against an objective rubric, scoring it out of 10 and diagnosing gaps without requiring manual human review.

### 4. Tech Stack Breakdown
| Technology | Role in Architecture |
| :--- | :--- |
| **LangChain** | LCEL chain composition (`|`), prompt templates, and agent abstraction |
| **OpenAI GPT-4o-mini** | High-speed, cost-effective reasoning engine for synthesis & evaluation |
| **Tavily Search API** | Real-time, AI-optimized web search engine |
| **BeautifulSoup4** | HTML parsing and boilerplate DOM stripping (scripts, navbars, footers) |
| **Streamlit** | Reactive frontend with custom dark UI and real-time execution state |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
