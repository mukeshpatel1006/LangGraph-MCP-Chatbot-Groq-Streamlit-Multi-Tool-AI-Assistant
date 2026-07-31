# LangGraph-MCP-Chatbot-Groq-Streamlit-Multi-Tool-AI-Assistant
An AI chatbot built with LangGraph, Groq, and MCP featuring multi-tool calling, persistent memory, streaming responses, DuckDuckGo search, stock market lookup, arithmetic tools, and a modern Streamlit interface.
# 🚀 LangGraph MCP Chatbot

A production-ready AI chatbot built using **LangGraph**, **Groq LLM**, **Model Context Protocol (MCP)**, and **Streamlit**.

The chatbot supports **tool calling**, **persistent conversation memory**, **multiple MCP servers**, **streaming responses**, and **SQLite checkpointing** to provide an intelligent conversational experience.

---

## 📌 Features

- 🤖 Groq Llama 3.3 70B Integration
- 🧠 LangGraph State Machine
- 🔄 Persistent Chat Memory using SQLite
- ⚡ Streaming AI Responses
- 🔧 Tool Calling
- 🌐 DuckDuckGo Search
- 📈 Live Stock Price Lookup
- ➗ Arithmetic MCP Server
- ☁️ Remote MCP Server Support
- 💬 Multi Conversation Threads
- 📂 Conversation History
- 🚀 Async Backend
- 🎯 Streamlit Chat Interface

---

# 🏗 Project Architecture

```
                    User
                      │
                      ▼
             Streamlit Frontend
                      │
                      ▼
              LangGraph Backend
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
      Chat Node              Tool Node
          │                       │
          ▼                       ▼
       Groq LLM              Available Tools
                              │
      ┌──────────┬──────────┬────────────┐
      ▼          ▼          ▼            ▼
 DuckDuckGo   Stock API   Math MCP   Expense MCP

                      │
                      ▼
             SQLite Checkpointer
```

---

# 📁 Project Structure

```
LangGraph-MCP-Chatbot/
│
├── langgraph_mcp_backend.py
├── langgraph_frontend_mcp.py
├── math_server.py
├── chatbot.db
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙ Backend

The backend is developed using **LangGraph**.

It is responsible for

- Loading the Groq LLM
- Registering tools
- Connecting to MCP Servers
- Managing conversation memory
- Streaming responses
- Tool execution
- SQLite checkpointing

### Tools

- DuckDuckGo Search
- Stock Price Tool
- Arithmetic MCP Server
- Expense MCP Server

---

# 🎨 Frontend

The frontend is built using **Streamlit**.

Features

- ChatGPT-like Interface
- Live Streaming Responses
- Conversation History
- Multiple Chat Threads
- Tool Status Display
- Persistent Conversations

---

# 🔄 Workflow

```
User

↓

Streamlit UI

↓

LangGraph

↓

Groq LLM

↓

Need Tool?

├── No
│
└── Yes
      │
      ▼
 Tool Node
      │
      ▼
 Execute Tool
      │
      ▼
 Tool Output
      │
      ▼
 Groq LLM
      │
      ▼
 Stream Response
```

---

# 🛠 Technologies Used

- Python
- LangGraph
- LangChain
- Groq API
- MCP (Model Context Protocol)
- Streamlit
- SQLite
- DuckDuckGo Search
- Alpha Vantage API
- AsyncIO

---

# 📦 Installation

Clone Repository

```bash
git clone https://github.com/yourusername/LangGraph-MCP-Chatbot.git
```

Move into project

```bash
cd LangGraph-MCP-Chatbot
```

Create Virtual Environment

### Windows

```bash
python -m venv myenv
```

Activate

```bash
myenv\Scripts\activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key

LANGCHAIN_API_KEY=your_langsmith_api_key

LANGCHAIN_TRACING_V2=true

LANGCHAIN_PROJECT=LangGraph MCP Chatbot
```

---

# ▶️ Run the Application

## Backend

```bash
python langgraph_mcp_backend.py
```

## Frontend

```bash
streamlit run langgraph_frontend_mcp.py
```

---

# 💬 Example Queries

```


Who is the CEO of NVIDIA?
✅ Tool finished

The CEO of NVIDIA is Jensen Huang

Hi how are you
I'm doing well, thanks for asking. Is there something I can help you with or would you like to chat?
calculate 567 multiply 4 is
The result of 567 multiplied by 4 is 2268.
Today Manipur temerature is ?
✅ Tool finished

The current temperature in Manipur is 28°C (82°F) during the day and 22°C (72°F) at night, with a chance of rain.

# ⭐ Future Improvements

- Voice Chat
- Image Understanding
- PDF RAG
- Authentication
- Multi User Support
- Docker Deployment
- Cloud Deployment
- Vector Database

---

# 👨‍💻 Author

**Mukesh Patel**

B.Tech CSE | Machine Learning | Generative AI | LangGraph | MCP | Agentic AI

GitHub:
https://github.com/mukeshpatel1006

LinkedIn:
https://www.linkedin.com/in/mukesh-patel-9aa41529a

---

## ⭐ Star this repository if you found it useful.
