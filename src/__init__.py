#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mcp[cli]>=1.15.0",
# ]
# ///

"""MCP Prompt Server - Exposes markdown files as MCP prompts."""

__version__ = "0.1.0"

from .server import main

if __name__ == "__main__":
    main()