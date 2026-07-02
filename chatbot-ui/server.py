import json
import httpx
import ollama
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

MCP_SERVER_URL = "http://localhost:5050"
OLLAMA_MODEL = "llama3.1"

SYSTEM_PROMPT = """You are a helpful UK government data assistant. You help users explore and understand public data collections about early years, education, childcare, and vaccinations.

You have access to two tools:
- get_all_content_no_data: Returns all guidance/content documents from collections (markdown files about early years, data manual, etc.)
- get_data: Returns all dataset files (statistics, vaccination coverage, childcare provider data)

When users ask about available data or want to explore what's there, use these tools to look up the information. Summarise the results clearly and concisely."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_all_content_no_data",
            "description": "Returns all content/guidance documents from collections, excluding raw data files. Use this to find information about early years topics, data standards, and guidance.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_data",
            "description": "Returns all data files (statistics, datasets) organised by type. Use this to find vaccination coverage data, education statistics, and childcare provider data.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


async def call_mcp_tool(tool_name: str) -> str:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{MCP_SERVER_URL}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": tool_name, "arguments": {}},
            },
        )
        result = response.json()
        if "result" in result:
            content = result["result"].get("content", [])
            texts = [c["text"] for c in content if c.get("type") == "text"]
            return "\n".join(texts)
        return json.dumps(result)


async def chat_with_tools(messages: list) -> str:
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=messages,
        tools=TOOLS,
    )

    msg = response["message"]

    if msg.get("tool_calls"):
        messages.append(msg)
        for tool_call in msg["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            tool_result = await call_mcp_tool(tool_name)
            messages.append({"role": "tool", "content": tool_result})

        follow_up = ollama.chat(model=OLLAMA_MODEL, messages=messages)
        return follow_up["message"]["content"]

    return msg["content"]


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    try:
        while True:
            user_msg = await ws.receive_text()
            messages.append({"role": "user", "content": user_msg})

            try:
                response = await chat_with_tools(messages)
                messages.append({"role": "assistant", "content": response})
                await ws.send_text(response)
            except Exception as e:
                await ws.send_text(f"Error: {str(e)}")
    except WebSocketDisconnect:
        pass


@app.get("/")
async def root():
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
