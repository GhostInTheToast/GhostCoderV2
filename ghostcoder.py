#!/usr/bin/env python3
"""
👻  GhostCoder (Python port)
A phantom developer that haunts your terminal, powered by a local Ollama server.

Feature parity with the original Bash version:
  • Uses OLLAMA_BASE_URL / OLLAMA_MODEL env‑vars
  • Options: -p/--print, -y/--yes, --no-apply, -h/--help
  • @filename substitution with full file‑content in prompt
  • Distinguishes modification vs. explanation requests
  • Shows diffs and asks confirmation (unless -y or --no-apply)
  • Interactive séance mode when no prompt is given
  • Automatically applies code blocks returned by the model

Requires: Python ≥3.8, requests, jq (optional for coloured diffs)
Licence: MIT – mirror of original project terms.
"""

from typing import List

from ai_client import send_prompt

# Import from modular structure
from cli import build_parser, interactive_loop
from setup import setup_environment


def main(argv: List[str] = None) -> None:
    """
    Main entry point for GhostCoder.
    
    Args:
        argv: Command line arguments (defaults to sys.argv)
    """
    args = build_parser().parse_args(argv)
    
    # Handle setup option
    if args.setup:
        setup_environment()
        return
    
    prompt = " ".join(args.prompt).strip()

    auto_apply = not (args.print_only or args.no_apply)

    if prompt:
        send_prompt(prompt, auto_apply, args.auto_yes, args.force_code)
    else:
        interactive_loop(auto_apply, args.auto_yes, args.force_code)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👻  The ghost fades back into the digital realm…")

