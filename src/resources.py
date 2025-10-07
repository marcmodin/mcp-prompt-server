"""
Resource Loading and Processing Module

Handles loading, parsing, and validating resource documents for MCP resources.

SECURITY:
- Resource content is returned as-is without sanitization. MCP clients should treat
  all resource content as potentially untrusted and apply appropriate sanitization
  before rendering or executing any content.
- File size is limited to 10MB to prevent resource exhaustion attacks.
- Path traversal protection ensures only files within the designated directory are loaded.
- Symlinks are resolved and validated to prevent directory escape.
"""

from pathlib import Path
from .utils import load_documents, ParsedDocument


def load_resource_documents(directory: Path) -> dict[str, tuple[ParsedDocument, str]]:
    """
    Load all resource documents from directory.
    Returns a dict mapping resource name to (ParsedDocument, source_path).

    Resources can have slashes in their names for URI-style paths (e.g., "docs/api").

    Raises:
        FileNotFoundError: If directory doesn't exist
        NotADirectoryError: If path is not a directory
    """
    resources = load_documents(
        directory=directory,
        file_extensions=['.md'],
        allow_slashes_in_name=True,
        document_type="resource"
    )

    return resources