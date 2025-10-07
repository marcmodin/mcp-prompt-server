# MCP Prompt Server - Architecture Documentation

## Overview

The MCP Prompt Server is a Python-based implementation of the Model Context Protocol (MCP) that dynamically exposes markdown files as MCP prompts. It provides a simple yet secure way to manage and serve prompt templates to MCP-compatible clients such as Claude Desktop.

## Purpose

The server enables:
- **Dynamic Prompt Management**: Load and expose markdown files as MCP prompts without code changes
- **Template Distribution**: Share prompt templates across teams and applications
- **Separation of Concerns**: Decouple prompt content from application logic
- **Standardized Interface**: Use MCP protocol for prompt discovery and retrieval

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        MCP Client                            │
│                    (e.g., Claude Desktop)                    │
└─────────────────────────┬───────────────────────────────────┘
                          │ MCP Protocol (stdio)
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   MCP Prompt Server                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              FastMCP Framework                       │   │
│  │          (Protocol Implementation)                   │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐   │
│  │         src/server.py (Main Entry Point)             │   │
│  │  - Initialize FastMCP instance ("file-prompts")      │   │
│  │  - Load prompts from prompts/                        │   │
│  │  - Load resources from resources/                    │   │
│  │  - Register prompt/resource handlers dynamically     │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐   │
│  │       src/prompts.py (Prompt Loading Module)         │   │
│  │  - Load markdown prompt files                        │   │
│  │  - Uses shared utils for validation                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │      src/resources.py (Resource Loading Module)      │   │
│  │  - Load markdown resource documents                  │   │
│  │  - Supports URI-style names (e.g., "docs/api")       │   │
│  │  - Uses shared utils for validation                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │       src/utils.py (Shared Utilities Module)         │   │
│  │  - Generic document loader (load_documents)          │   │
│  │  - Parse YAML frontmatter                            │   │
│  │  - Validate security constraints                     │   │
│  │  - Path sanitization for logging                     │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                      │
└───────────────────────┼──────────────────────────────────────┘
                        │
           ┌────────────┴────────────┐
           │                         │
┌──────────▼──────────┐   ┌─────────▼──────────┐
│  prompts/ Directory │   │ resources/ Directory│
│ *.md files with YAML│   │ *.md files with YAML│
│     frontmatter     │   │     frontmatter     │
└─────────────────────┘   └────────────────────┘
```

### Component Architecture

#### 1. **src/server.py** - Main Entry Point

**Responsibilities:**

- Initialize the FastMCP server instance with name "file-prompts"
- Load markdown prompts from the `prompts/` directory
- Load markdown resources from the `resources/` directory
- Dynamically register prompt and resource handlers using closures
- Use `importlib.resources` for reliable path resolution (with fallback)
- Start the MCP server with stdio transport

**Key Design Patterns:**

- **Closure Pattern**: Each prompt handler is created via closure to capture specific content and description
- **Dynamic Registration**: Prompts are registered at runtime based on filesystem content

```python
def create_prompt_handler(prompt_content: str, prompt_desc: str):
    def handler() -> str:
        return prompt_content
    handler.__doc__ = prompt_desc
    return handler
```

#### 2. **src/prompts.py** - Prompt Loading Module

**Responsibilities:**

- Load markdown files from `prompts/` directory using shared utilities
- Wrapper around `load_documents()` with prompt-specific configuration
- Enforces that no valid prompts results in fatal error

#### 3. **src/resources.py** - Resource Loading Module

**Responsibilities:**

- Load markdown files from `resources/` directory using shared utilities
- Supports URI-style names with forward slashes (e.g., "docs/api")
- Configurable file size limit (can be larger than prompts if needed)
- Returns empty dict if resources directory doesn't exist (non-fatal)

#### 4. **src/utils.py** - Shared Utilities Module

**Responsibilities:**

- Generic document loading function (`load_documents()`)
- YAML frontmatter parsing with security constraints
- Path validation and sanitization for logging
- Configurable file size limits per document type

**Security Features:**

- Path traversal protection via `Path.is_relative_to()`
- Symlink rejection (checked before resolution to prevent TOCTOU)
- Configurable file size limits (default: 10MB via `DEFAULT_MAX_FILE_SIZE_BYTES`)
- Hard-coded name/description length limits (`MAX_NAME_LENGTH`, `MAX_DESCRIPTION_LENGTH`)
- Input validation with configurable character restrictions
- ReDoS prevention (frontmatter parsing limited to first 100 lines)
- Sanitized logging to prevent information leakage

#### 5. **FastMCP Framework Integration**

The server leverages the MCP Python SDK's FastMCP framework for:

- MCP protocol implementation
- Transport handling (stdio)
- Prompt registration and lifecycle management
- Client communication

### Data Flow

```
1. Server Initialization
   ├─ Load markdown files from prompts/
   ├─ Parse frontmatter (name, description)
   ├─ Validate security constraints
   └─ Register prompt handlers

2. Client Connection
   ├─ MCP handshake via stdio
   ├─ Capability negotiation
   └─ Client ready

3. Prompt Discovery (list_prompts)
   ├─ Client requests available prompts
   └─ Server returns list with names & descriptions

4. Prompt Retrieval (get_prompt)
   ├─ Client requests specific prompt by name
   ├─ Server executes registered handler
   └─ Returns markdown content
```

## Design Principles

### 1. Security-First Design

**Path Security:**

- All file paths are resolved and validated to prevent directory traversal
- Symlinks are explicitly rejected (before resolution to prevent TOCTOU)
- `Path.is_relative_to()` ensures files remain within designated directories
- `importlib.resources` used for reliable path resolution across installation types

**Resource Limits:**
- Default maximum file size: 10MB (`DEFAULT_MAX_FILE_SIZE_BYTES`)
- Configurable per document type (via `max_file_size` parameter)
- Hard-coded maximum name length: 100 characters (`MAX_NAME_LENGTH`)
- Hard-coded maximum description length: 200 characters (`MAX_DESCRIPTION_LENGTH`)

**Input Validation:**
- Prompt names restricted to: `[a-zA-Z0-9_-\s]`
- Resource names allow forward slashes for URIs: `[a-zA-Z0-9_-\s/]`
- No path traversal sequences (`..`, `\`) allowed
- YAML frontmatter parsing limited to first 100 lines (DoS prevention)

**Logging Security:**
- Paths sanitized before logging to prevent information leakage
- Generic error messages for security violations

### 2. Simplicity and Maintainability

- Single-purpose components with clear responsibilities
- Minimal dependencies (MCP SDK + PyYAML)
- Standard YAML parsing with PyYAML library
- Fail-fast error handling

### 3. Extensibility

- **Directory-based**: Add prompts by creating markdown files
- **Hot-reload ready**: Architecture supports future file watching
- **Metadata extensible**: Frontmatter can support additional fields

### 4. MCP Protocol Compliance

- Implements MCP prompt primitives
- Uses stdio transport for client communication
- Follows FastMCP patterns and conventions

## Technical Requirements

### Runtime Requirements

- **Python**: ≥3.11
- **Package Manager**: `uv` (recommended) or `pip`
- **Dependencies**:
  - `mcp[cli]>=1.15.0` (Model Context Protocol SDK)
  - `pyyaml>=6.0` (YAML parsing)

### Development Requirements

```bash
# Install dependencies
uv sync

# Run server
uv run mcp-prompt-server

# Debug with MCP Inspector
npx @modelcontextprotocol/inspector uv --directory [path] run mcp-prompt-server
```

### Deployment Requirements

**File Structure:**
```
mcp-prompt-server/
├── src/
│   ├── __init__.py        # Package initialization
│   ├── server.py          # Main entry point (main function)
│   ├── prompts.py         # Prompt loading logic
│   ├── resources.py       # Resource loading logic
│   └── utils.py           # Shared utilities (validation, parsing)
├── prompts/               # Markdown prompt files
│   └── *.md               # Prompts with YAML frontmatter
├── resources/             # Markdown resource documents
│   └── *.md               # Resources with YAML frontmatter
├── pyproject.toml         # Project configuration
├── local.mcp.json         # MCP client config (local dev)
└── remote.mcp.json        # MCP client config (remote)
```

**MCP Client Configuration**:

For remote usage (recommended):
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

For local development:
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

### Security Requirements

1. **File System Access**:
   - Read-only access to `prompts/` directory
   - No write operations required
   - No network access required

2. **Resource Constraints**:
   - Bounded memory usage (10MB per file)
   - O(n) startup time where n = number of markdown files
   - No recursive prompt loading (single directory level)

3. **Input Validation**:
   - All user-controlled input validated
   - Path traversal prevention
   - No code execution from prompt content

## Prompt File Format

### Required Structure

```yaml
---
name: prompt-name
description: Brief description of what this prompt does
---

# Prompt Content

The actual prompt content goes here. This can include:
- Multiple lines
- Markdown formatting
- Code blocks
- Lists and other markdown features
```

### Frontmatter Fields

| Field | Required | Type | Max Length | Description |
|-------|----------|------|------------|-------------|
| `name` | Yes | String | 100 chars | Unique prompt identifier (alphanumeric, dash, underscore, space) |
| `description` | Yes | String | 200 chars | Human-readable description for MCP clients (2-3 sentences) |
| `arguments` | No | List[Object] | - | Optional list of prompt arguments (see below) |

### Prompt Arguments (Optional)

Prompts can define arguments for dynamic content substitution:

```yaml
---
name: code-explainer
description: Explains code with optional difficulty level
arguments:
  - name: code
    description: The code snippet to explain
    required: true
  - name: difficulty
    description: Target audience level (beginner/intermediate/advanced)
    required: false
---

Please explain the following code:

```
{code}
```

{difficulty}
```

**Argument Object Fields:**

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `name` | Yes | String | - | Argument name (alphanumeric and underscore only) |
| `description` | No | String | `None` | Human-readable description of the argument |
| `required` | No | Boolean | `false` | Whether the argument must be provided |

**Note:** Arguments use `{argument_name}` syntax for template substitution in the prompt content.

### Content Processing

- **No Sanitization**: Markdown content returned as-is
- **Client Responsibility**: MCP clients must sanitize before rendering
- **Encoding**: UTF-8 required

## Operational Characteristics

### Startup Behavior

1. Server validates `prompts/` directory exists
2. Lists `.md` files in top-level directory only (using `os.listdir`)
3. Parses and validates each file
4. Registers successful prompts
5. Logs warnings for invalid files
6. Fails if zero valid prompts found

### Runtime Behavior

- **Stateless**: No runtime state modification
- **Immutable Prompts**: Changes require server restart
- **Error Handling**: Invalid files skipped with warnings
- **Performance**: O(1) prompt retrieval after initialization

### Error Handling Strategy

| Error Type | Behavior |
|------------|----------|
| Missing `prompts/` | Fatal - Server exits with error |
| Invalid markdown file | Warning logged - File skipped |
| Path traversal attempt | Warning logged - File skipped |
| File size exceeded | Warning logged - File skipped |
| Invalid frontmatter | Warning logged - File skipped |
| No valid prompts | Fatal - Server exits with error |

## Limitations and Considerations

### Current Limitations

1. **No Hot-Reload**: Changes to markdown files require server restart
2. **Flat Directory Structure**: Only loads from top-level `prompts/` directory (no subdirectory scanning)
3. **Startup-Only Loading**: Prompts loaded once at initialization

### Future Enhancement Opportunities

1. **File Watching**: Implement hot-reload using file system watchers
2. **Subdirectory Support**: Enable recursive directory traversal
3. **Caching Layer**: Add file modification time tracking
4. **Metrics**: Add prometheus metrics for prompt usage
5. **Multi-transport**: Support SSE/HTTP transports alongside stdio

## Security Considerations

### Threat Model

**Protected Against:**
- ✅ Path traversal attacks
- ✅ Symlink-based directory escape
- ✅ Resource exhaustion (file size limits)
- ✅ ReDoS in frontmatter parsing
- ✅ Information leakage via logs

**Client Responsibility:**
- ⚠️ XSS prevention (markdown rendering)
- ⚠️ Content sanitization
- ⚠️ Access control (MCP client level)

### Defense-in-Depth Layers

1. **Input Validation**: Name/description format checks
2. **Path Validation**: Resolve and verify all paths
3. **Resource Limits**: File size and string length constraints
4. **Error Handling**: Generic error messages externally
5. **Logging Security**: Sanitized path information

## Monitoring and Observability

### Logging Strategy

- **Level**: INFO (default)
- **Format**: `%(levelname)s: %(message)s`
- **Content**:
  - Startup validation
  - Prompt loading warnings
  - Security violations
  - Fatal errors

### Key Metrics (Future)

- Number of prompts loaded
- Load failures by reason
- Prompt retrieval frequency
- Average file size

## Compliance and Standards

- **MCP Specification**: Compliant with MCP protocol
- **Python Standards**: PEP 8, PEP 484 (type hints)
- **Security**: OWASP File Upload/Path Traversal guidelines
- **Logging**: No sensitive data in logs

## References
- @docs/mcp-python-sdk.md
- [MCP Python SDK Documentation](https://modelcontextprotocol.github.io/python-sdk/)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [FastMCP Framework](https://github.com/modelcontextprotocol/python-sdk)
