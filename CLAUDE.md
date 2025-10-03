# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that exposes markdown files as prompts to MCP clients. It dynamically loads markdown files from the `commands/` directory and registers them as prompts via the FastMCP framework.

## Architecture

### Core Components

- **`mcp_prompt_server/server.py`**: Main entry point that initializes the FastMCP server, loads prompts from `commands/`, and dynamically registers them using closures. Each markdown file becomes a prompt handler.
- **`mcp_prompt_server/prompts.py`**: Handles markdown file loading, YAML frontmatter parsing, and security validation. Contains strict path traversal protection, file size limits (10MB), and input validation for prompt names and descriptions.

### Prompt Format

Markdown files in `commands/` must include YAML frontmatter:
```yaml
---
name: prompt-name
description: Brief description
---

# Prompt Content
...
```

The `name` and `description` fields are required. Names must be alphanumeric with dashes, underscores, or spaces only.

### Security Model

The codebase has extensive security measures:
- Path traversal protection using `Path.resolve()` and `is_relative_to()` checks
- Symlinks are explicitly rejected
- File size limited to 10MB (MAX_FILE_SIZE_BYTES)
- Name/description length limits (MAX_NAME_LENGTH=200, MAX_DESCRIPTION_LENGTH=1000)
- Sanitized logging to prevent path information leakage
- No markdown content sanitization (responsibility delegated to MCP clients)

## Development Commands

### Running locally
```bash
uv run mcp-prompt-server
```

### Debugging with MCP Inspector
```bash
npx @modelcontextprotocol/inspector uv --directory [path] run mcp-prompt-server
```

### Package management
This project uses `uv` for dependency management. Dependencies are defined in `pyproject.toml`.

## MCP Integration

The server is configured as an MCP stdio server in `server.mcp.json`:
```json
{
  "mcpServers": {
    "prompt-server": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "mcp-prompt-server"]
    }
  }
}
```

## Key Constraints

- Python >=3.11 required
- All markdown files must be in `commands/` directory (no subdirectory recursion currently implemented, but os.walk is used)
- Prompt registration happens at server startup; changes require restart
- The unused import `sanitize_path_for_logging` in server.py:13 can be removed as it's only used internally in prompts.py