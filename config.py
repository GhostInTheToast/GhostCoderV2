#!/usr/bin/env python3
"""
Configuration module for GhostCoder.
Contains all constants, environment variables, and configuration settings.
"""

import os
import re

# --------------------------------------------------------------------------- #
#  Configuration                                                               #
# --------------------------------------------------------------------------- #
BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "deepseek-coder:6.7b-instruct")

MODIFICATION_WORDS = {
    "rewrite", "fix", "add", "remove", "delete", "update", "change",
    "modify", "refactor", "improve", "optimize", "convert", "replace",
    "implement", "create", "write", "generate", "make", "build",
}

EXPLANATION_WORDS = {
    "explain", "describe", "what", "how", "why", "analyze", "review",
    "understand", "show me", "tell me", "look at",
}

CODE_BLOCK_RE = re.compile(r"```(?:\w+)?\s*\n(.*?)```", re.DOTALL)
FILE_REF_RE = re.compile(r"@([A-Za-z0-9._/-]+)")

# System prompt to encourage code generation
SYSTEM_PROMPT = """You are GhostCoder, a coding assistant that specializes in generating actual code changes and implementations.

IMPORTANT GUIDELINES:
- When asked to modify, fix, or implement something, ALWAYS provide the complete code in code blocks
- Don't just explain what to do - show the actual code changes
- If modifying existing files, provide the complete updated file content
- Use proper code block syntax with language specification when possible
- Be direct and actionable - focus on implementation over explanation
- If you need to explain something, do it briefly and then show the code

Your responses should be practical and ready to use.""" 