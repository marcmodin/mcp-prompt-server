# Contributing Guide

## Installation Options

### Remote (Recommended for Users)

Run directly from GitHub without cloning:

```bash
# Run from GitHub
uvx --from git+https://github.com/marcmodin/mcp-prompt-server mcp-prompt-server

# Debug from GitHub
npx @modelcontextprotocol/inspector uvx --from git+https://github.com/marcmodin/mcp-prompt-server mcp-prompt-server
```

### Local (For Development)

Clone the repository and run locally:

```bash
# Run locally
uv run mcp-prompt-server

# Debug locally
npx @modelcontextprotocol/inspector uv --directory [path] run mcp-prompt-server
```

## Development Workflow

### Adding New Prompts

1. Open project in Claude Code with the mcp loaded (see `remote.mcp.json` for reference)
2. Use `/prompt-server:create-prompt` and follow instructions to create a new prompt
3. Restart Claude to reload the MCP server with the new prompt
4. Test the prompt execution thoroughly

### Code Changes & Commits

All changes (code or prompts) require proper git workflow:

1. Use `/prompt-server:git-workflow-assistant` to commit changes to a new branch
2. Open a pull request for review
3. Squash merge to `main` to create a new release version

### Tracking Issues & Features

For bugs or feature requests that don't require immediate implementation:

1. Use `/prompt-server:create-github-issue` to generate a new issue
2. Track and prioritize for later implementation
3. No git commit required until implementation begins

## Testing

- **Prompt Testing**: Always test prompts thoroughly after creation and before committing
- **Server Restart**: Remember that prompt changes require server restart to take effect
- **MCP Inspector**: Use MCP Inspector for debugging (see commands above)

## Pull Request Guidelines

- Use descriptive branch names
- Write clear commit messages
- Squash merge to main to keep history clean
- Each PR should represent a single logical change

## Code Standards

- Python >=3.11
- Follow existing code patterns and security measures
- See [architecture.md](architecture.md) for security requirements
- Use `uv` for dependency management
