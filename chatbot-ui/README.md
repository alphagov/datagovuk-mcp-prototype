# Data Collection Chatbot UI

Chat interface for exploring UK government data collections, powered by Ollama (Llama 3.1) and connected to the MCP server.

## Prerequisites

1. **Ollama** installed and running:
   ```bash
   brew install ollama
   ollama pull llama3.1
   ```

2. **MCP server** running on port 5050:
   ```bash
   cd ../collections-mcp
   python server.py
   ```

## Setup

```bash
pip install -r requirements.txt
python server.py
```

Open http://localhost:8000 in your browser.

## How it works

- Browser connects to the Python backend via WebSocket
- Backend sends user messages to Ollama with tool definitions
- When Ollama decides to use a tool, the backend calls the MCP server
- Results are sent back to Ollama to generate a natural language response
- Response is streamed back to the browser
