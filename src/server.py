#!/usr/bin/env python3
"""
MCP Prompt Server - Python Implementation

Loads markdown files from the prompts directory and exposes them as MCP prompts.

"""

import logging
from pathlib import Path
from importlib.resources import files

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
    for name, (description, content, _) in prompts_data.items():
        # Create a closure to capture the current values
        def create_prompt_handler(prompt_content: str, prompt_desc: str):
            def handler() -> str:
                return prompt_content
            handler.__doc__ = prompt_desc
            return handler

        # Register the prompt with FastMCP
        prompt_handler = create_prompt_handler(content, description)
        mcp.prompt(name)(prompt_handler)

    # Dynamically register each resource document
    for name, (description, content, _) in resources_data.items():
        # Create a closure to capture the current values
        def create_resource_handler(resource_content: str, resource_desc: str):
            def handler() -> str:
                return resource_content
            handler.__doc__ = resource_desc
            return handler

        # Register the resource with FastMCP
        resource_handler = create_resource_handler(content, description)
        mcp.resource(f"resource://{name}", name=name)(resource_handler)

    # Register ping tool
    @mcp.tool()
    def ping() -> str:
        """Simple ping tool that returns pong"""
        return "pong"

    # Run the server
    mcp.run(transport="stdio")

