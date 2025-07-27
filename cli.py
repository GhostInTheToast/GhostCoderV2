#!/usr/bin/env python3
"""
Command Line Interface module for GhostCoder.
Handles argument parsing and interactive mode.
"""

import argparse

from ai_client import send_prompt
from config import BASE_URL, MODEL


def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the command line argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    p = argparse.ArgumentParser(
        prog="ghostcoder",
        description="👻  GhostCoder ‑ your phantom coding assistant (Python edition)",
        add_help=False,
        epilog="""
Examples:
  ghostcoder "fix the bug in @main.py"
  ghostcoder --code "implement a login system"
  ghostcoder --skip-confirm "add error handling to @utils.py"
  ghostcoder --no-apply "explain how this code works"
  ghostcoder --setup  # Run setup wizard
        """,
    )
    p.add_argument("-p", "--print", dest="print_only", action="store_true")
    p.add_argument("--skip-confirm", dest="auto_yes", action="store_true",
                   help="Skip confirmation prompts and auto-apply changes")
    p.add_argument("--no-apply", dest="no_apply", action="store_true")
    p.add_argument("--code", dest="force_code", action="store_true",
                   help="Force the ghost to return code changes instead of explanations")
    p.add_argument("--setup", action="store_true",
                   help="Run setup wizard to configure environment and aliases")
    p.add_argument("-h", "--help", action="help")
    p.add_argument("prompt", nargs=argparse.REMAINDER, help="Prompt for the ghost")
    return p


def interactive_loop(auto_apply: bool, auto_yes: bool, force_code: bool = False) -> None:
    """
    Run the interactive loop for GhostCoder.
    
    Args:
        auto_apply: Whether to automatically apply code changes
        auto_yes: Whether to automatically confirm changes
        force_code: Whether to force code generation mode
    """
    print("👻  GhostCoder – Interactive séance mode (type 'exit' to banish)")
    print(f"Connected to spectral realm: {BASE_URL}")
    print(f"Phantom model: {MODEL}")
    if force_code:
        print("🔧  Force-code mode: Ghost will prioritize code generation")
    print("💡  Use @filename to show files to the ghost\n")

    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break
        if user_input.strip().lower() in {"exit", "quit", "banish"}:
            break
        if user_input:
            print("👻  GhostCoder:", end=" ")
            send_prompt(user_input, auto_apply, auto_yes, force_code)
            print() 