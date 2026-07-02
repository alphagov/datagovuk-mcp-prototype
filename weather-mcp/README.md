# Weather MCP Server

An MCP server providing weather forecasts and alerts using the US National Weather Service API and Open-Meteo for global coverage.

## Tools

- **get_alerts** — Get active weather alerts for a US state (two-letter code, e.g. `CA`)
- **get_forecast** — Get a forecast for a US location by latitude/longitude (uses NWS)
- **get_global_forecast** — Get a forecast for any location worldwide by latitude/longitude (uses Open-Meteo)

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- [Node.js](https://nodejs.org/) (for MCP Inspector)

## Setup

```bash
uv sync
```

## Running the server

```bash
uv run mcp run weather.py
```

## Running with MCP Inspector

The MCP Inspector provides a web UI to test and debug your MCP server interactively:

```bash
npx @modelcontextprotocol/inspector uv run mcp run weather.py
```

- `npx @modelcontextprotocol/inspector` — downloads and launches the Inspector web UI (requires Node.js/npm installed)
- `uv run mcp run weather.py` — this is the command the Inspector spawns as a subprocess to start your MCP server

This opens a browser at `http://localhost:6274` where you can:

1. See all available tools
2. Call tools with custom parameters
3. Inspect request/response payloads

## Adding to Claude Code

Add to your `.claude/settings.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/weather-mcp", "mcp", "run", "weather.py"]
    },
    "collections": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/datagovuk-mcp", "python", "server.py"]
    }
  }
}
```
