"""
Shared Utilities for Loading and Validating Documents

Provides common validation, parsing, and security functions used by both
prompts and resources modules.

SECURITY:
- Content is returned as-is without sanitization. MCP clients should treat
  all content as potentially untrusted and apply appropriate sanitization
  before rendering or executing any content.
- File size is limited to 10MB to prevent resource exhaustion attacks.
- Path traversal protection ensures only files within the designated directory are loaded.
- Symlinks are resolved and validated to prevent directory escape.
"""

import os
import re
import logging
from pathlib import Path
from typing import Callable

# Configure logging
logger = logging.getLogger(__name__)

# Security constants - these are hard limits that cannot be overridden
MAX_NAME_LENGTH = 100  # Maximum length for names
MAX_DESCRIPTION_LENGTH = 200  # Maximum length for descriptions

# Default file size limit (can be overridden per document type)
DEFAULT_MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB default limit


def validate_safe_name(name: str, allow_slashes: bool = False) -> None:
    """
    Validate that a name is safe and doesn't contain path traversal sequences.

    Args:
        name: The name to validate
        allow_slashes: Whether to allow forward slashes (useful for URIs)

    Raises:
        ValueError: If validation fails
    """
    # Check length
    if len(name) > MAX_NAME_LENGTH:
        raise ValueError(f"Name exceeds maximum length of {MAX_NAME_LENGTH}")

    # Check for path traversal sequences
    if '..' in name or '\\' in name:
        raise ValueError("Name contains invalid path characters")

    # Build regex pattern based on whether slashes are allowed
    if allow_slashes:
        pattern = r'^[a-zA-Z0-9_\-\s/]+$'
    else:
        pattern = r'^[a-zA-Z0-9_\-\s]+$'

    if not re.match(pattern, name):
        allowed = "alphanumeric, dash, underscore, slash, and spaces" if allow_slashes else "alphanumeric, dash, underscore, and spaces"
        raise ValueError(f"Name contains invalid characters (only {allowed} allowed)")


def parse_frontmatter(content: str, allow_slashes_in_name: bool = False) -> tuple[str, str, str]:
    """
    Parse YAML frontmatter from content.

    Args:
        content: The file content with frontmatter
        allow_slashes_in_name: Whether to allow slashes in the name field

    Returns:
        Tuple of (name, description, content_without_frontmatter)

    Raises:
        ValueError: If frontmatter is missing or invalid
    """
    # Split content by lines to avoid ReDoS with large inputs
    lines = content.split('\n')

    # Check if content starts with frontmatter delimiter
    if not lines or lines[0].strip() != '---':
        raise ValueError("No valid frontmatter found")

    # Find the closing delimiter (limit search to first 100 lines to prevent DoS)
    closing_index = None
    for i in range(1, min(len(lines), 100)):
        if lines[i].strip() == '---':
            closing_index = i
            break

    if closing_index is None:
        raise ValueError("No closing frontmatter delimiter found")

    # Extract frontmatter and body
    frontmatter_lines = lines[1:closing_index]
    body_lines = lines[closing_index + 1:]
    body = '\n'.join(body_lines)

    # Parse simple YAML key-value pairs
    name = None
    description = None

    for line in frontmatter_lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key == 'name':
                name = value
            elif key == 'description':
                description = value

    if not name or not description:
        raise ValueError("Frontmatter must include 'name' and 'description'")

    # Validate name and description lengths
    if len(name) > MAX_NAME_LENGTH:
        raise ValueError(f"Name exceeds maximum length of {MAX_NAME_LENGTH}")

    if len(description) > MAX_DESCRIPTION_LENGTH:
        raise ValueError(f"Description exceeds maximum length of {MAX_DESCRIPTION_LENGTH}")

    # Validate name is safe (no path traversal)
    validate_safe_name(name, allow_slashes=allow_slashes_in_name)

    return name, description, body


def sanitize_path_for_logging(path: Path, base_dir: Path) -> str:
    """
    Sanitize file path for logging to prevent information leakage.

    Args:
        path: The path to sanitize
        base_dir: The base directory to make the path relative to

    Returns:
        A relative path string or a generic identifier
    """
    try:
        return str(path.relative_to(base_dir))
    except ValueError:
        return "<file outside base directory>"


def load_documents(
    directory: Path,
    file_extensions: list[str],
    allow_slashes_in_name: bool = False,
    document_type: str = "document",
    max_file_size: int = DEFAULT_MAX_FILE_SIZE_BYTES
) -> dict[str, tuple[str, str, str]]:
    """
    Generic document loader that handles validation and security checks.

    Args:
        directory: The directory to load documents from
        file_extensions: List of allowed file extensions (e.g., ['.md', '.txt'])
        allow_slashes_in_name: Whether to allow slashes in document names
        document_type: Type of document being loaded (for logging)
        max_file_size: Maximum file size in bytes (default: 10MB)

    Returns:
        Dict mapping document name to (description, content, source_path)

    Raises:
        FileNotFoundError: If directory doesn't exist
        NotADirectoryError: If path is not a directory
    """
    dir_path = directory.resolve()

    # Validate directory exists
    if not dir_path.exists():
        raise FileNotFoundError(f"{document_type.capitalize()} directory not found")

    if not dir_path.is_dir():
        raise NotADirectoryError(f"{document_type.capitalize()} path is not a directory")

    documents = {}

    # Only load from top-level directory (no recursive traversal)
    for filename in os.listdir(dir_path):
        # Check file extension
        if not any(filename.endswith(ext) for ext in file_extensions):
            continue

        doc_file = dir_path / filename

        try:
            # Check if it's a symlink (skip symlinks for security)
            # IMPORTANT: Check BEFORE resolving to prevent TOCTOU attacks
            if doc_file.is_symlink():
                sanitized_path = sanitize_path_for_logging(doc_file, dir_path)
                logger.warning(f"Skipping {sanitized_path}: symlinks not allowed")
                continue

            # Resolve the file path and validate it's within the base directory
            resolved_file = doc_file.resolve()

            # Security check: ensure resolved path is still within base directory
            if not resolved_file.is_relative_to(dir_path):
                sanitized_path = sanitize_path_for_logging(doc_file, dir_path)
                logger.warning(f"Skipping {sanitized_path}: path traversal detected")
                continue

            # Check file size before reading
            file_size = doc_file.stat().st_size
            if file_size > max_file_size:
                sanitized_path = sanitize_path_for_logging(doc_file, dir_path)
                logger.warning(f"Skipping {sanitized_path}: file exceeds size limit ({file_size} > {max_file_size} bytes)")
                continue

            content = doc_file.read_text(encoding='utf-8')

            # Parse frontmatter to extract name, description, and body
            name, description, body = parse_frontmatter(content, allow_slashes_in_name=allow_slashes_in_name)

            documents[name] = (description, body, str(doc_file))

        except (ValueError, OSError):
            # Sanitize error message to avoid leaking sensitive paths
            sanitized_path = sanitize_path_for_logging(doc_file, dir_path)
            logger.warning(f"Failed to load {sanitized_path}: validation error")
            continue
        except Exception:
            # Generic error for unexpected issues
            sanitized_path = sanitize_path_for_logging(doc_file, dir_path)
            logger.warning(f"Failed to load {sanitized_path}: unexpected error")
            continue

    if not documents:
        logger.info(f"No valid {document_type} files found in {sanitize_path_for_logging(dir_path, dir_path.parent)}")

    return documents