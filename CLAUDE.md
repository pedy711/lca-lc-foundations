# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Companion repository for LangChain Academy's "Introduction to LangChain" course. Contains Jupyter notebooks organized into three progressive modules covering LangChain, LangGraph, and agent development patterns.

## Common Commands

```bash
# Install dependencies (uv recommended)
uv sync

# Verify environment setup (checks Python version, packages, API keys)
uv run python env_utils.py

# Run Jupyter notebooks
uv run jupyter lab

# Run LangGraph Studio (from notebooks/module-1 or notebooks/module-3)
uv run langgraph dev
```

## Environment

- **Python:** >=3.12, <3.14 (strictly enforced)
- **Package manager:** uv (recommended) or pip
- **API keys:** Configured in `.env` at project root (copy from `example.env`)
  - Required: `OPENAI_API_KEY`, `TAVILY_API_KEY`
  - Optional: `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `LANGSMITH_API_KEY`
- Notebooks load env vars via `load_dotenv()` — keys don't need to be set globally

## Repository Structure

```
notebooks/
  module-1/   # Create Agent: foundational models, tools, memory, multimodal
  module-2/   # Advanced Agent: MCP, state management, multi-agent systems
  module-3/   # Production-Ready Agent: HITL, dynamic agents, email assistant
```

Each module contains numbered lesson notebooks (e.g., `1.1_foundational_models.ipynb`). Modules 1 and 3 also have standalone Python agent files (`1.5_personal_chef.py`, `3.5_email_agent.py`) used with LangGraph Studio via `langgraph.json` configs.

## Key Patterns

- **Model initialization:** Uses `init_chat_model()` for model-agnostic code, primarily `gpt-5-nano`
- **Agent creation:** Uses `create_agent()` with tools and system prompts
- **Tool definition:** `@tool` decorator with type hints and docstrings
- **Environment loading:** Every notebook starts with `from dotenv import load_dotenv; load_dotenv()`
- **LangGraph Studio:** Configured per-module in `langgraph.json`, referencing agent entry points and `../../.env`
- **MCP server:** Module 2 includes a custom MCP server at `notebooks/module-2/resources/2.1_mcp_server.py`
