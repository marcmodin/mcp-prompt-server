<div align="center">

# 🚀 MCP Prompt Server

**A lightweight Model Context Protocol server for dynamic prompt management**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

---

## ✨ Features

- 📁 **Dynamic Prompt Loading** — Automatically discover and register markdown files from the `prompts/` directory
- ⚡ **Zero Configuration** — Add prompts by simply creating markdown files with YAML frontmatter
- 🔒 **Security First** — Built-in path traversal protection, file size limits, and input validation
- 🎯 **MCP Compliant** — Full implementation of MCP prompt primitives via FastMCP framework
- 🌐 **Remote Installation** — Run directly from GitHub without cloning

## 🔧 Requirements

- Python >=3.11
- Package manager: `uv` (installs automatically with `uvx`)

## Quick Start

### Using with Claude Cli

Add this configuration to your Claude Cli MCP settings:

```json
{
  "mcpServers": {
    "prompt-server": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/marcmodin/mcp-prompt-server",
        "mcp-prompt-server"
      ]
    }
  }
}
```

### Using with GitHub Copilot

Create `.vscode/mcp.json` in your project:

```json
{
  "mcpServers": {
    "prompt-server": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/marcmodin/mcp-prompt-server",
        "mcp-prompt-server"
      ]
    }
  }
}
```

### Running Remotely

```bash
# Run directly from GitHub
uvx --from git+https://github.com/marcmodin/mcp-prompt-server mcp-prompt-server

# Debug with MCP Inspector
npx @modelcontextprotocol/inspector uvx --from git+https://github.com/marcmodin/mcp-prompt-server mcp-prompt-server
```

## 📚 Documentation

- **[Architecture](docs/architecture.md)** — System design and security model
- **[Contributing](docs/contributing.md)** — Development workflow and guidelines
- **[Prompt Template](docs/prompt-template.md)** — Creating prompt files
