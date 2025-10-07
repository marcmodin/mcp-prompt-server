"""
Prompt Loading and Processing Module

Handles loading, parsing, and validating markdown files for MCP prompts.

SECURITY:
- Markdown content is returned as-is without sanitization. MCP clients should treat
  all prompt content as potentially untrusted and apply appropriate sanitization
  before rendering or executing any content.
- File size is limited to 10MB to prevent resource exhaustion attacks.
- Path traversal protection ensures only files within the designated directory are loaded.
- Symlinks are resolved and validated to prevent directory escape.
"""

from pathlib import Path
from .utils import load_documents, ParsedDocument


def load_markdown_prompts(directory: Path) -> dict[str, tuple[ParsedDocument, str]]:
    """
    Load all markdown files from directory.
    Returns a dict mapping prompt name to (ParsedDocument, source_path).

    Raises:
        FileNotFoundError: If directory doesn't exist
        NotADirectoryError: If path is not a directory
        ValueError: If no valid markdown files found
    """
    prompts = load_documents(
        directory=directory,
        file_extensions=['.md'],
        allow_slashes_in_name=False,
        document_type="prompt",
        parse_arguments=True
    )

    if not prompts:
        raise ValueError(f"No valid .md files found")

    return prompts