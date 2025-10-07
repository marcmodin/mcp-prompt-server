"""
Shared Utilities for Loading and Validating Documents

Handles loading, parsing, and validating markdown files for MCP prompts and resources.

SECURITY:
- Markdown content is returned as-is without sanitization. MCP clients should treat
  all content as potentially untrusted and apply appropriate sanitization
  before rendering or executing any content.
- File size is limited to 10MB to prevent resource exhaustion attacks.
- Path traversal protection ensures only files within the designated directory are loaded.
- Symlinks are resolved and validated to prevent directory escape.
"""

import os
import re
import logging
import yaml
from pathlib import Path
from dataclasses import dataclass

# Configure logging
logger = logging.getLogger(__name__)

# Security constants - these are hard limits that cannot be overridden
MAX_NAME_LENGTH = 100  # Maximum length for names
MAX_DESCRIPTION_LENGTH = 200  # Maximum length for descriptions

# Default file size limit (can be overridden per document type)
DEFAULT_MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB default limit


@dataclass
class PromptArgument:
    """Represents a prompt argument definition compatible with MCP spec."""
    name: str
    description: str | None = None
    required: bool = False


@dataclass
class ParsedDocument:
    """Result of parsing a document's frontmatter."""
    name: str
    description: str
    content: str
    arguments: list[PromptArgument] | None = None


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


def parse_frontmatter(content: str, allow_slashes_in_name: bool = False, parse_arguments: bool = False) -> ParsedDocument:
    """
    Parse YAML frontmatter from content.

    Args:
        content: The file content with frontmatter
        allow_slashes_in_name: Whether to allow slashes in the name field
        parse_arguments: Whether to parse the arguments field (for prompts)

    Returns:
        ParsedDocument with extracted metadata and content

    Raises:
        ValueError: If frontmatter is missing or invalid
    """
    lines = content.split('\n')

    if not lines or lines[0].strip() != '---':
        raise ValueError("No valid frontmatter found")

    # Find closing delimiter (limit to first 100 lines to prevent DoS)
    closing_index = None
    for i in range(1, min(len(lines), 100)):
        if lines[i].strip() == '---':
            closing_index = i
            break

    if closing_index is None:
        raise ValueError("No closing frontmatter delimiter found")

    frontmatter_text = '\n'.join(lines[1:closing_index])
    body = '\n'.join(lines[closing_index + 1:])

    # Parse YAML frontmatter using PyYAML
    try:
        fields = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in frontmatter: {e}")

    # Extract required fields
    name = fields.get('name')
    description = fields.get('description')

    if not name or not description:
        raise ValueError("Frontmatter must include 'name' and 'description'")

    if not isinstance(name, str) or not isinstance(description, str):
        raise ValueError("'name' and 'description' must be strings")

    # Validate lengths
    if len(name) > MAX_NAME_LENGTH:
        raise ValueError(f"Name exceeds maximum length of {MAX_NAME_LENGTH}")

    if len(description) > MAX_DESCRIPTION_LENGTH:
        raise ValueError(f"Description exceeds maximum length of {MAX_DESCRIPTION_LENGTH}")

    # Validate name is safe
    validate_safe_name(name, allow_slashes=allow_slashes_in_name)

    # Parse arguments if requested (for prompts)
    arguments = None
    if parse_arguments:
        arguments_raw = fields.get('arguments')
        if arguments_raw is not None:
            if not isinstance(arguments_raw, list):
                raise ValueError("arguments must be a list")

            arguments = []
            for arg in arguments_raw:
                if not isinstance(arg, dict):
                    raise ValueError("Each argument must be an object with 'name' field")

                arg_name = arg.get('name')
                if not arg_name or not isinstance(arg_name, str):
                    raise ValueError("Argument must have a 'name' field (string)")

                if not re.match(r'^[a-zA-Z0-9_]+$', arg_name):
                    raise ValueError(f"Invalid argument name '{arg_name}' (only alphanumeric and underscore allowed)")

                # Optional fields with SDK defaults
                arg_description = arg.get('description')  # Default: None
                if arg_description is not None and not isinstance(arg_description, str):
                    raise ValueError(f"Argument description must be a string for '{arg_name}'")

                arg_required = arg.get('required', False)  # SDK default: False
                if not isinstance(arg_required, bool):
                    raise ValueError(f"Argument 'required' must be a boolean for '{arg_name}'")

                arguments.append(PromptArgument(
                    name=arg_name,
                    description=arg_description,
                    required=arg_required
                ))

    return ParsedDocument(
        name=name,
        description=description,
        content=body,
        arguments=arguments
    )


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
    max_file_size: int = DEFAULT_MAX_FILE_SIZE_BYTES,
    parse_arguments: bool = False
) -> dict[str, tuple[ParsedDocument, str]]:
    """
    Generic document loader that handles validation and security checks.

    Args:
        directory: The directory to load documents from
        file_extensions: List of allowed file extensions (e.g., ['.md', '.txt'])
        allow_slashes_in_name: Whether to allow slashes in document names
        document_type: Type of document being loaded (for logging)
        max_file_size: Maximum file size in bytes (default: 10MB)
        parse_arguments: Whether to parse arguments field (for prompts)

    Returns:
        Dict mapping document name to (ParsedDocument, source_path)

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

            # Parse frontmatter
            parsed = parse_frontmatter(
                content,
                allow_slashes_in_name=allow_slashes_in_name,
                parse_arguments=parse_arguments
            )

            documents[parsed.name] = (parsed, str(doc_file))

        except (ValueError, OSError) as e:
            sanitized_path = sanitize_path_for_logging(doc_file, dir_path)
            logger.warning(f"Failed to load {sanitized_path}: {str(e)}")
            continue
        except Exception as e:
            sanitized_path = sanitize_path_for_logging(doc_file, dir_path)
            logger.warning(f"Failed to load {sanitized_path}: {str(e)}")
            continue

    if not documents:
        logger.info(f"No valid {document_type} files found in {sanitize_path_for_logging(dir_path, dir_path.parent)}")

    return documents