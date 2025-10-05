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

There are three approaches for adding new prompts:

#### Approach 1: Direct Implementation (Recommended for Contributors)

1. Open project in Claude Code
2. Use `/create-prompt` (claude command) and follow instructions to create a new prompt
3. Restart Claude to reload the MCP server with the new prompt
4. Test the prompt execution thoroughly
5. Commit changes using the git workflow

#### Approach 2: AI-Assisted Prompt Request (Recommended for Users)

Use the conversational prompt request assistant:

1. Use `/create-prompt-issue-request` (claude command) in Claude Code
2. The assistant will guide you through providing all necessary information
3. A GitHub issue will be created automatically with all details filled in
4. A developer or AI agent can then implement the prompt based on the request

#### Approach 3: Manual GitHub Issue (Alternative)

Submit a prompt request directly on GitHub:

1. Go to the [GitHub Issues](https://github.com/marcmodin/mcp-prompt-server/issues/new/choose) page
2. Select "Prompt Request" template
3. Fill in all required fields manually
4. Submit the issue for review and implementation

**When to use each approach:**

- **Approach 1**: You have development access and want to implement immediately
- **Approach 2**: You prefer guided, conversational workflow with validation
- **Approach 3**: You prefer working directly in GitHub's web interface

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
- See @docs/mcp-python-sdk.md for sdk related information
- See @docs/architecture.md for security requirements
- Use `uv` for dependency management

### Commit Message Guidelines

This project follows [Conventional Commits](https://www.conventionalcommits.org/) specification.

**Supported Types:**

- `feat:` - New feature or functionality
- `fix:` - Bug fix or security patch
- `docs:` - Documentation changes only
- `refactor:` - Code refactoring without functional changes
- `chore:` - Maintenance tasks (dependencies, config, etc.)
- `ci:` - CI/CD pipeline changes
- `revert:` - Revert a previous commit

**Format:**

```yaml
<type>: <short description>

<optional body>

<optional footer>
```

**Examples:**

```bash
feat: add support for subdirectory prompt organization
fix: prevent path traversal in symlink resolution
docs: update architecture with new security constraints
refactor: simplify frontmatter parsing logic
chore: update mcp sdk to v1.16.0
```

**Best Practices:**

- Use imperative mood ("add" not "added")
- Keep subject line under 72 characters
- Separate subject from body with blank line
- Use body to explain what and why, not how
- Reference issues/PRs in footer when applicable
