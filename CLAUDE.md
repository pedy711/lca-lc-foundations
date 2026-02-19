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

# Run the MCP server for module 2 (requires uv for uvx)
uvx notebooks/module-2/resources/2.1_mcp_server.py

# Run the agent chat UI (from notebooks/module-3/agent-chat-ui)
pnpm install && pnpm dev
```

## Environment

- **Python:** >=3.12, <3.14 (strictly enforced)
- **Package manager:** uv (recommended) or pip; `uv` is also required in Module 2 Lesson 1 to run the MCP server with `uvx`
- **API keys:** Configured in `.env` at project root (copy from `example.env`)
  - Required: `OPENAI_API_KEY`, `TAVILY_API_KEY`
  - Optional: `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY` (only used in Module 1 Lesson 1)
  - Optional: `LANGSMITH_API_KEY` (for evaluation/tracing)
- Notebooks load env vars via `load_dotenv()` — keys don't need to be set globally

## Repository Structure

```
notebooks/
  module-1/               # Create Agent
    1.1–1.4 notebooks     # Foundational models, tools, memory, multimodal
    1.5_personal_chef.py  # Standalone agent for LangGraph Studio
    langgraph.json        # LangGraph Studio config → 1.5_personal_chef.py:agent
  module-2/               # Advanced Agent
    2.1–2.4 notebooks     # MCP, state/context, multi-agent, wedding planner project
    bonus_rag.ipynb       # RAG with PDF (uses resources/acmecorp-employee-handbook.pdf)
    bonus_sql.ipynb       # SQL agent (uses resources/Chinook.db)
    resources/            # MCP server, sample DB, sample PDF
  module-3/               # Production-Ready Agent
    3.2–3.5 notebooks     # Managing messages, HITL, dynamic agents, email assistant
    3.5_email_agent.py    # Standalone agent for LangGraph Studio
    langgraph.json        # LangGraph Studio config → 3.5_email_agent.py:agent
    agent-chat-ui/        # Next.js chat UI (separate app, uses pnpm)
```

## Key Patterns

- **Model initialization:** Uses `init_chat_model()` for model-agnostic code, primarily `gpt-5-nano`
- **Agent creation:** `create_agent(model, tools, system_prompt)` from `langchain.agents` — the core abstraction used throughout
- **Tool definition:** `@tool` decorator with type hints and docstrings; tools can accept `runtime: ToolRuntime` to access context and `tool_call_id`
- **Environment loading:** Every notebook/script starts with `from dotenv import load_dotenv; load_dotenv()`
- **LangGraph Studio:** Configured per-module in `langgraph.json`, referencing agent entry points and `../../.env`

## Architecture (Module 3 Agent Patterns)

The email agent (`3.5_email_agent.py`) demonstrates the full production pattern:

- **Custom state:** Extend `AgentState` with additional fields (e.g., `AuthenticatedState` adds `authenticated: bool`)
- **Context schemas:** `@dataclass` context injected into tools via `ToolRuntime.context` — configured via `context_schema` param on `create_agent`
- **Tool → state updates:** Tools return `Command(update={...})` to modify agent state directly (e.g., setting `authenticated=True`)
- **Middleware stack:** `create_agent(..., middleware=[...])` accepts:
  - `@wrap_model_call` — intercepts model calls to dynamically swap tools based on state
  - `@dynamic_prompt` — generates system prompts based on current state
  - `HumanInTheLoopMiddleware(interrupt_on={...})` — selectively requires human approval per tool

## MCP Server (Module 2)

`notebooks/module-2/resources/2.1_mcp_server.py` uses `FastMCP` from the `mcp` package with three primitives: `@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()`. Run via stdio transport.
