#!/usr/bin/env python3
"""
MCP Prompt Server - Python Implementation

Loads markdown files from the commands directory and exposes them as MCP prompts.

"""

import logging
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from .prompts import load_markdown_prompts, sanitize_path_for_logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Commands directory path
COMMANDS_DIR = Path(__file__).parent.parent / "commands"


def main() -> int:
    """Main entry point for the MCP server."""

    # Load prompts from directory
    try:
        prompts_data = load_markdown_prompts(COMMANDS_DIR)
    except Exception as e:
        logger.error(f"Failed to load prompts: {e}")
        return 1

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

    # Run the server
    mcp.run(transport="stdio")

