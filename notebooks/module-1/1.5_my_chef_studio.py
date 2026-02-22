from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient

tavily_client = TavilyClient()

MODEL_NAME = "gemini-2.5-flash-lite"

model = init_chat_model(model=MODEL_NAME, model_provider="google_genai")

@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)

system_prompt = """You are a personal chef assistant. The user will show you the contents of their fridge
and give you voice instructions about what they'd like to eat. Based on the available ingredients
and the user's request, suggest recipes and cooking instructions. Use web search to find recipes if needed."""

agent = create_agent(
    model=model,
    tools=[web_search],
    system_prompt=system_prompt
)
