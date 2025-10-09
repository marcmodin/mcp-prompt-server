#!/usr/bin/env python3
"""
MCP Prompt Server - Python Implementation

Loads markdown files from the prompts directory and exposes them as MCP prompts.
"""

import inspect
import logging
from pathlib import Path
from importlib.resources import files
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from .prompts import load_markdown_prompts
from .resources import load_resource_documents

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Directory paths - using importlib.resources for reliable path resolution
try:
    prompts_ref = files("prompts")
    # Handle both regular Path and MultiplexedPath from importlib.resources
    if hasattr(prompts_ref, '__fspath__'):
        PROMPTS_DIR = Path(prompts_ref.__fspath__())
    else:
        # For MultiplexedPath, iterate to get first valid path
        PROMPTS_DIR = Path(next(iter(prompts_ref._paths)))
    logger.info(f"Loaded prompts from package: {PROMPTS_DIR}")
except (TypeError, ModuleNotFoundError, AttributeError, StopIteration) as e:
    # Fallback for development mode
    PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
    logger.info(f"Using fallback prompts path: {PROMPTS_DIR}")

try:
    resources_ref = files("resources")
    # Handle both regular Path and MultiplexedPath from importlib.resources
    if hasattr(resources_ref, '__fspath__'):
        RESOURCES_DIR = Path(resources_ref.__fspath__())
    else:
        # For MultiplexedPath, iterate to get first valid path
        RESOURCES_DIR = Path(next(iter(resources_ref._paths)))
    logger.info(f"Loaded resources from package: {RESOURCES_DIR}")
except (TypeError, ModuleNotFoundError, AttributeError, StopIteration) as e:
    # Fallback for development mode
    RESOURCES_DIR = Path(__file__).parent.parent / "resources"
    logger.info(f"Using fallback resources path: {RESOURCES_DIR}")


def create_prompt_handler(content: str, description: str, arguments: list | None = None):
    """
    Create a prompt handler function with the appropriate signature.

    Follows introspection pattern using inspect.Signature and
    proper annotations.

    For prompts without arguments, returns a simple function.
    For prompts with arguments, creates a function with expected parameters
    and signature that FastMCP can introspect.

    Args:
        content: The prompt template content
        description: The prompt description (becomes the function docstring)
        arguments: Optional list of PromptArgument objects

    Returns:
        A callable handler function with proper signature and annotations
    """
    if not arguments:
        # Simple handler for prompts without arguments
        def handler() -> str:
            return content
        handler.__doc__ = description
        return handler

    # Create handler that will be called with validated args
    def handler(**kwargs) -> str:
        """Template handler with dynamic parameters."""
        
        # Perform substitution
        result = content
        for arg_name, arg_value in kwargs.items():
            result = result.replace(f'{{{arg_name}}}', str(arg_value))
        return result

    # Build parameters with proper annotations for introspection
    parameters = []
    annotations = {}

    for arg in arguments:
        # Use Annotated to embed description metadata
        if arg.description:
            annotation = Annotated[str, arg.description]
        else:
            annotation = str

        # Create Parameter object
        param = inspect.Parameter(
            name=arg.name,
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=inspect.Parameter.empty,  # Required parameter
            annotation=annotation
        )

        parameters.append(param)
        annotations[arg.name] = annotation

    # Create and attach signature (FastMCP calls inspect.signature())
    handler.__signature__ = inspect.Signature(
        parameters=parameters,
        return_annotation=str
    )

    # Set annotations and docstring
    annotations['return'] = str
    handler.__annotations__ = annotations
    handler.__doc__ = description

    return handler


def main() -> int:
    """Main entry point for the MCP server."""

    # Load prompts from directory
    try:
        prompts_data = load_markdown_prompts(PROMPTS_DIR)
    except Exception as e:
        logger.error(f"Failed to load prompts: {e}")
        return 1

    # Load resources from directory
    try:
        resources_data = load_resource_documents(RESOURCES_DIR)
    except Exception as e:
        logger.warning(f"Failed to load resources: {e}")
        resources_data = {}

    # Create FastMCP server
    mcp = FastMCP("file-prompts")

    # Dynamically register each markdown file as a prompt
    for name, (parsed_doc, _) in prompts_data.items():
        logger.info(f"Registering prompt: {name}")

        handler = create_prompt_handler(
            content=parsed_doc.content,
            description=parsed_doc.description,
            arguments=parsed_doc.arguments
        )

        mcp.prompt(name)(handler)

    # Dynamically register each resource document
    for name, (parsed_doc, _) in resources_data.items():
        def create_resource_handler(resource_content: str, resource_desc: str):
            def handler() -> str:
                return resource_content
            handler.__doc__ = resource_desc
            return handler

        resource_handler = create_resource_handler(parsed_doc.content, parsed_doc.description)
        mcp.resource(f"resource://{name}", name=name)(resource_handler)

    # Register ping tool
    @mcp.tool()
    def ping() -> str:
        """Simple ping tool that returns pong"""
        return "pong"

    # Run the server
    mcp.run(transport="stdio")