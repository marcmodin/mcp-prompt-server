# AGENTS.md

Agent instructions for working in this repository.

## Quick Reference

**Architecture**: See [docs/architecture.md](docs/architecture.md) for complete system design and security model.

**Contributing**: See [docs/contributing.md](docs/contributing.md) for development workflow and contribution guidelines.

**Run locally**: `uv run mcp-prompt-server`

**Debug**: `npx @modelcontextprotocol/inspector uv --directory [path] run mcp-prompt-server`

## Key Constraints

- Python >=3.11, uses `uv` for dependency management
- Prompt files must be in `prompts/` with required YAML frontmatter (name, description)
- Changes to markdown files require server restart