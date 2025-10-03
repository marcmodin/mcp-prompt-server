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

import os
import re
import logging
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

# Security constants
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB limit for markdown files
MAX_NAME_LENGTH = 200  # Maximum length for prompt name
MAX_DESCRIPTION_LENGTH = 1000  # Maximum length for description


def validate_safe_name(name: str) -> None:
    """
    Validate that a prompt name is safe and doesn't contain path traversal sequences.
    Raises ValueError if validation fails.
    """
    # Check length
    if len(name) > MAX_NAME_LENGTH:
        raise ValueError(f"Name exceeds maximum length of {MAX_NAME_LENGTH}")

    # Check for path traversal sequences
    if '..' in name or '/' in name or '\\' in name:
        raise ValueError("Name contains invalid path characters")

    # Allow only alphanumeric, dash, underscore, and spaces
    if not re.match(r'^[a-zA-Z0-9_\-\s]+$', name):
        raise ValueError("Name contains invalid characters (only alphanumeric, dash, underscore, and spaces allowed)")


def parse_frontmatter(content: str) -> tuple[str, str, str]:
    """
    Parse YAML frontmatter from markdown content.
    Returns (name, description, content_without_frontmatter).
    Raises ValueError if frontmatter is missing or invalid.
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
    validate_safe_name(name)

    return name, description, body


def sanitize_path_for_logging(path: Path, base_dir: Path) -> str:
    """
    Sanitize file path for logging to prevent information leakage.
    Returns a relative path from base_dir or a generic identifier.
    """
    try:
        return str(path.relative_to(base_dir))
    except ValueError:
        return "<file outside base directory>"


def load_markdown_prompts(directory: Path) -> dict[str, tuple[str, str, str]]:
    """
    Load all markdown files from directory.
    Returns a dict mapping prompt name to (description, content, source_path).
    """
    dir_path = directory.resolve()

    # Validate directory exists
    if not dir_path.exists():
        raise FileNotFoundError(f"Commands directory not found")

    if not dir_path.is_dir():
        raise NotADirectoryError(f"Commands path is not a directory")

    prompts = {}

    # Walk through directory without following symlinks to avoid TOCTOU
    for root, _, files in os.walk(dir_path, followlinks=False):
        root_path = Path(root)

        for filename in files:
            if not filename.endswith('.md'):
                continue

            md_file = root_path / filename

            try:
                # Resolve the file path and validate it's within the base directory
                resolved_file = md_file.resolve()

                # Security check: ensure resolved path is still within base directory
                if not resolved_file.is_relative_to(dir_path):
                    sanitized_path = sanitize_path_for_logging(md_file, dir_path)
                    logger.warning(f"Skipping {sanitized_path}: path traversal detected")
                    continue

                # Check if it's a symlink (skip symlinks for security)
                if md_file.is_symlink():
                    sanitized_path = sanitize_path_for_logging(md_file, dir_path)
                    logger.warning(f"Skipping {sanitized_path}: symlinks not allowed")
                    continue

                # Check file size before reading
                file_size = md_file.stat().st_size
                if file_size > MAX_FILE_SIZE_BYTES:
                    sanitized_path = sanitize_path_for_logging(md_file, dir_path)
                    logger.warning(f"Skipping {sanitized_path}: file exceeds size limit")
                    continue

                content = md_file.read_text(encoding='utf-8')

                # Parse frontmatter to extract name, description, and body
                name, description, body = parse_frontmatter(content)

                prompts[name] = (description, body, str(md_file))

            except (ValueError, OSError):
                # Sanitize error message to avoid leaking sensitive paths
                sanitized_path = sanitize_path_for_logging(md_file, dir_path)
                logger.warning(f"Failed to load {sanitized_path}: validation error")
                continue
            except Exception:
                # Generic error for unexpected issues
                sanitized_path = sanitize_path_for_logging(md_file, dir_path)
                logger.warning(f"Failed to load {sanitized_path}: unexpected error")
                continue

    if not prompts:
        raise ValueError(f"No valid .md files found")

    return prompts