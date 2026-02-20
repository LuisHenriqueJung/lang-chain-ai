from typing import Any
from langchain_openai import ChatOpenAI
from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime

from dotenv import load_dotenv

load_dotenv()
messages = []

# Access memory
@tool
def get_user_info(user_id: str, runtime: ToolRuntime) -> str:
    """Look up user info."""
    store = runtime.store
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

# Update memory
@tool
def save_user_info(user_id: str, user_info: dict[str, Any], runtime: ToolRuntime) -> str:
    """Save user info."""
    store = runtime.store
    store.put(("users",), user_id, user_info)
    return "Successfully saved user info."


store = InMemoryStore()
model = ChatOpenAI(model="gpt-4.1")
agent = create_agent(
    model,
    tools=[get_user_info, save_user_info],
    store=store
)
