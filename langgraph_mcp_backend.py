# langgraph_mcp_backend.py

import asyncio
import sys
import threading
from typing import Annotated, TypedDict

import aiosqlite
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import BaseTool, tool
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
import requests

load_dotenv()

# Dedicated async loop for backend tasks
_ASYNC_LOOP = asyncio.new_event_loop()
_ASYNC_THREAD = threading.Thread(target=_ASYNC_LOOP.run_forever, daemon=True)
_ASYNC_THREAD.start()


def _submit_async(coro):
    return asyncio.run_coroutine_threadsafe(coro, _ASYNC_LOOP)


def run_async(coro):
    return _submit_async(coro).result()


def submit_async_task(coro):
    """Schedule a coroutine on the backend event loop."""
    return _submit_async(coro)


# -------------------
# 1. LLM (Groq)
# -------------------
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# -------------------
# 2. Tools
# -------------------


# Custom wrapper for search to prevent Groq schema parsing errors
@tool
def search_tool(query: str) -> str:
    """Search the web for current events, news, or general information."""
    ddg = DuckDuckGoSearchRun(region="us-en")
    return ddg.run(query)


@tool
def get_stock_price(symbol: str) -> dict:
    """Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA')

    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    r = requests.get(url)
    return r.json()


client = MultiServerMCPClient(
    {
        "arith": {
            "transport": "stdio",
            "command": sys.executable,  # Uses active python interpreter
            "args": [
                "c:/Users/Mukesh Patel/Desktop/LangGraph-Chatbot/math_server.py"
            ],
        },
        "expense": {
            "transport": "streamable_http",  # if this fails, try "sse"
            "url": "https://splendid-gold-dingo.fastmcp.app/mcp",
        },
    }
)


def load_mcp_tools() -> list[BaseTool]:
    try:
        return run_async(client.get_tools())
    except Exception:
        return []


mcp_tools = load_mcp_tools()

tools = [search_tool, get_stock_price, *mcp_tools]
llm_with_tools = llm.bind_tools(tools) if tools else llm


# -------------------
# 3. State & System Prompt
# -------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


SYSTEM_PROMPT = SystemMessage(
    content="You are a helpful assistant with access to search, stock price, and arithmetic tools. "
    "Always strictly format tool call argument values to conform to expected JSON schemas."
)


# -------------------
# 4. Nodes
# -------------------
async def chat_node(state: ChatState):
    """LLM node that may answer or request a tool call."""
    messages = state["messages"]

    # Sanitize tool message contents to prevent Groq 400 Bad Request errors
    sanitized_messages = []
    for msg in messages:
        if isinstance(msg, ToolMessage):
            content = msg.content
            if (
                content is None
                or content == ""
                or (isinstance(content, list) and len(content) == 0)
            ):
                content = "Tool executed successfully with no content returned."
            elif not isinstance(content, (str, list)):
                content = str(content)

            sanitized_messages.append(
                ToolMessage(
                    content=content,
                    tool_call_id=msg.tool_call_id,
                    name=getattr(msg, "name", None),
                    status=getattr(msg, "status", "success"),
                )
            )
        else:
            sanitized_messages.append(msg)

    if not sanitized_messages or not isinstance(
        sanitized_messages[0], SystemMessage
    ):
        sanitized_messages = [SYSTEM_PROMPT] + sanitized_messages

    response = await llm_with_tools.ainvoke(sanitized_messages)
    return {"messages": [response]}


tool_node = ToolNode(tools) if tools else None


# -------------------
# 5. Checkpointer
# -------------------
async def _init_checkpointer():
    conn = await aiosqlite.connect(database="chatbot.db")
    cp = AsyncSqliteSaver(conn)
    await cp.setup()  # Ensures tables are initialized
    return cp


checkpointer = run_async(_init_checkpointer())

# -------------------
# 6. Graph
# -------------------
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")

if tool_node:
    graph.add_node("tools", tool_node)
    graph.add_conditional_edges("chat_node", tools_condition)
    graph.add_edge("tools", "chat_node")
else:
    graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)


# -------------------
# 7. Helper
# -------------------
async def _alist_threads():
    all_threads = set()
    async for checkpoint in checkpointer.alist(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)


def retrieve_all_threads():
    return run_async(_alist_threads())