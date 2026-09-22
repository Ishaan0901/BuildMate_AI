# BuildMate AI

**Learn. Build. Share.**

BuildMate AI takes a developer's learning or project description and runs it through a parallel LangGraph workflow to generate three things at once: practical next-project ideas, a ready-to-publish GitHub README, and a LinkedIn post about what you built.

## Overview

Most developers finish a project and stop there — the idea for what to build next, the README, and the "share it with your network" post all get done separately, if at all. BuildMate AI runs three specialized AI agents in parallel on a single input (what you learned + what you built) and returns all three outputs in one pass.

## Features

- **Project Idea Advisor** – suggests 3 new, meaningfully different project ideas that extend what you just learned, ordered from beginner to more challenging.
- **GitHub README Agent** – writes a clean, copy-paste-ready `README.md` for the project described, using only information you actually provided.
- **LinkedIn Post Agent** – drafts a natural, non-corporate LinkedIn post about your learning journey, with relevant hashtags.
- **Parallel execution** – all three agents run concurrently via a LangGraph fan-out/fan-in graph, not sequentially.
- **Premium Streamlit UI** – dark, glassmorphic interface with copyable outputs for the README and LinkedIn post.

## Technologies Used

- **Python**
- **LangGraph** – state graph orchestration for the parallel agent workflow
- **LangChain (langchain-groq)** – LLM integration
- **Groq (Llama 3.3 70B Versatile)** – underlying language model
- **Streamlit** – frontend UI
- **python-dotenv** – environment variable management

## How It Works

1. The user describes what they learned and what they built.
2. A `StateGraph` fans the input out to three independent nodes: `advice_node`, `github_node`, and `linkedin_node`.
3. Each node prompts the LLM with a role-specific system prompt and returns its result into a shared `info` dict via a custom reducer.
4. All three branches fan back in to `END`, and the graph returns the combined results.
5. The Streamlit UI (`app.py`) imports the compiled graph from `project.py`, invokes it with the user's input, and renders the three outputs as separate cards.

## Installation

```bash
git clone https://github.com/<your-username>/buildmate-ai.git
cd buildmate-ai
pip install -r requirements.txt
```

Create a `.env` file in the project root with your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

## Usage

Run the workflow directly from the command line:
```bash
python project.py
```

Or launch the Streamlit UI:

```bash
streamlit run app.py
```

Then open the local URL Streamlit prints in your browser, describe what you learned and built, and click **Generate**.

## Project Structure

```text
BuildMate_AI/
│
├── project.py        # LangGraph workflow (agents, graph, state)
├── app.py             # Streamlit UI
├── .env               # API key (not committed)
└── requirements.txt
```

## Future Improvements

- Export generated outputs (README, LinkedIn post) directly to `.md` / `.txt` files
- Add support for additional LLM providers
- Let users pick which of the three agents to run
- Persist generation history per session
