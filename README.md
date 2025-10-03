# MCP Prompt Server

## Development 

Running the mcp_prompt_server locally
```
uv run mcp-prompt-server
```

Running MCP Inspector with the mcp_prompt_server using local project directory for debugging (couldnt get `uv run mcp dev` to work)
```
npx @modelcontextprotocol/inspector uv --directory [path] run mcp-prompt-server
```