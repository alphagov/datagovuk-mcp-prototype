# Datagovuk MCP Prototype

A collection of MCP servers used for prototyping.

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- [Node.js](https://nodejs.org/) (for MCP Inspector)

## Prototypes

### datagovuk-mcp

MCP server using the collections data from the data.gov.uk website.

### weather

MCP server showing weather reports for the US and globally taken from the <MCP website>[https://modelcontextprotocol.io/docs/develop/build-server].

## Testing the Dockerised MCP server locally with Claude Code

1. Build the Docker image

``` bash
cd datagovuk-mcp
docker build -t datagovuk-mcp .
```

2. Remove the default claude MCP

Comment out the datagovuk-mcp value in `.claude/settings.json`


Remove datagovuk-mcp from Claude
``` bash
claude mcp remove datagovuk-mcp
```

3. Run claude CLI command to add it as an MCP

``` bash
claude mcp add collections-docker-mcp -- docker run -i --rm datagovuk-mcp
```

4. Check that Claude is using the docker MCP

```
do you have access to collections-docker-mcp?
```

5. Tidy up

Uncomment the datagovuk-mcp in  `.claude/settings.json`

Remove collections-docker-mcp from Claude
``` bash
claude mcp remove collections-docker-mcp
```

Add the datagovuk-mcp back into Claude

``` bash
claude mcp add collections-mc
```
