# MCP Prompt Server

A lightweight Model Context Protocol (MCP) server that dynamically exposes markdown files as prompts to MCP-compatible clients like Claude Desktop.

## Features

- **Dynamic Prompt Loading**: Automatically discover and register markdown files from the `prompts/` directory
- **Zero Configuration**: Add prompts by simply creating markdown files with YAML frontmatter
- **Security First**: Built-in path traversal protection, file size limits, and input validation
- **MCP Compliant**: Full implementation of MCP prompt primitives via FastMCP framework

## Quick Start

```bash
# Run locally
uv run mcp-prompt-server

# Debug with MCP Inspector
npx @modelcontextprotocol/inspector uv --directory [path] run mcp-prompt-server
```

## Documentation

- [Architecture](docs/architecture.md) - System design and security model
- [Contributing](docs/contributing.md) - Development workflow and guidelines
- [Prompt Template](docs/prompt-template.md) - Creating prompt files

## Requirements

- Python >=3.11
- Package manager: `uv` (recommended) or `pip`