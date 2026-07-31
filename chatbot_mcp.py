# chatbot_mcp.py

import asyncio
import sys
from typing import TypedDict, Annotated
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

# -------------------
# 1. LLM (Groq)
# -------------------
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# -------------------
# 2. MCP Client
# -------------------
client = MultiServerMCPClient(
    {
        "arith": {
            "transport": "stdio",
            "command": sys.executable,  # Points automatically to your myenv Python interpreter
            "args": ["c:/Users/Mukesh Patel/Desktop/LangGraph-Chatbot/math_server.py"],
        }
    }
)

# -------------------
# 3. State Schema
# -------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

SYSTEM_PROMPT = SystemMessage(
    content="You are a helpful assistant with tool access. When using the calculator, operation MUST be one of: 'add', 'sub', 'mul', 'div', 'mod'."
)

async def build_graph():
    tools = await client.get_tools()
    llm_with_tools = llm.bind_tools(tools)

    # 4. Nodes
    async def chat_node(state: ChatState):
        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SYSTEM_PROMPT] + messages

        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    tool_node = ToolNode(tools)

    # 5. Graph
    graph = StateGraph(ChatState)
    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges("chat_node", tools_condition)
    graph.add_edge("tools", "chat_node")

    return graph.compile()


async def main():
    chatbot = await build_graph()

    result = await chatbot.ainvoke({
        "messages": [HumanMessage(content="Find the modulus if 132354 and 23 and give answer like a cricket commentator.")]
    })

    print("\n--- Answer ---")
    print(result['messages'][-1].content)

if __name__ == '__main__':
    asyncio.run(main())