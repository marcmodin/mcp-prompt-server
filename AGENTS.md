# AGENTS.md

Agent instructions for working in this repository.

## Quick Reference

**Architecture**: See [docs/architecture.md](docs/architecture.md) for complete system design and security model.

**Contributing**: See [docs/contributing.md](docs/contributing.md) for development workflow and contribution guidelines.

**Run locally**: `uv run mcp-prompt-server`

**Run remotely**: `uvx --from git+https://github.com/marcmodin/mcp-prompt-server mcp-prompt-server`

**Debug locally**: `npx @modelcontextprotocol/inspector uv run mcp-prompt-server`

**Debug remotely**: `npx @modelcontextprotocol/inspector uvx --from git+https://github.com/marcmodin/mcp-prompt-server mcp-prompt-server`

## Key Constraints

- Python >=3.11, uses `uv` for dependency management
- Prompt files must be in `prompts/` with required YAML frontmatter (name, description)
- Resource files must be in `resources/` with required YAML frontmatter (name, description)
- No symlinks allowed for security reasons
- Changes to markdown files require server restart