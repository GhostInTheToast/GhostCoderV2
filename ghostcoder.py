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
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple

try:
    import requests
except ImportError:  # pragma: no cover
    sys.exit("❌  'requests' not found – run: pip install requests")

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

# --------------------------------------------------------------------------- #
#  Helpers                                                                     #
# --------------------------------------------------------------------------- #
def is_modification_request(prompt: str) -> bool:
    lower = prompt.lower()
    if any(w in lower for w in EXPLANATION_WORDS):
        return False
    return any(w in lower for w in MODIFICATION_WORDS)


def read_file(path: Path) -> str:
    try:
        return path.read_text()
    except Exception as exc:  # pragma: no cover
        return f"[Error reading {path}: {exc}]"


def colour_diff(lines: List[str]) -> None:
    """Pretty‑print a unified diff, using colordiff if available."""
    colordiff = shutil.which("colordiff")
    if colordiff:
        proc = subprocess.run(
            [colordiff, "-u", "-"], input="".join(lines).encode(), check=False
        )
        if proc.returncode in (0, 1):
            return
    # Fallback: plain text
    sys.stdout.writelines(lines)


def process_file_references(prompt: str, force_code: bool = False) -> Tuple[str, bool, bool]:
    """
    Replace @filename tokens with embedded file blocks.

    Returns:
        processed_prompt : str
        has_file_refs    : bool
        is_modification  : bool
    """
    is_mod = is_modification_request(prompt) or force_code
    has_refs = False
    processed = prompt

    for match in FILE_REF_RE.finditer(prompt):
        has_refs = True
        filename = match.group(1)
        path = Path(filename)
        if path.exists():
            replacement = (
                f"\nFile: {filename}\n```"
                f"\n{read_file(path)}\n```"
            )
        else:
            replacement = f"[File '{filename}' not found]"
        processed = processed.replace(f"@{filename}", replacement, 1)

    # Enhanced prompt engineering for more agentic behavior
    if has_refs and is_mod:
        processed += (
            "\n\nCRITICAL: You are being asked to modify code. You MUST respond with the complete updated file content in a code block. "
            "Do not just explain what to change - show the actual code with all changes applied. "
            "Provide the entire file content, not just the modified parts."
        )
    elif is_mod and not has_refs:
        processed += (
            "\n\nIMPORTANT: This is a code modification request. Please provide the complete implementation in code blocks. "
            "Show the actual code, not just explanations of what to do."
        )
    
    return processed, has_refs, is_mod


def extract_code_for_file(response: str, filename: str | None = None) -> str:
    """
    Try to pull the relevant code block for a given filename from the model response.
    If filename is None, return the first code block found.
    """
    # Fast path: pick first block if no specific file requested.
    blocks = CODE_BLOCK_RE.findall(response)
    if not blocks:
        return ""

    if filename is None:
        return blocks[0].strip()

    # Look for a block that mentions the filename in the preceding few lines.
    lines = response.splitlines()
    for i, line in enumerate(lines):
        if filename in line:
            # search forward for ``` start
            for j in range(i, len(lines)):
                if lines[j].startswith("```"):
                    # capture until closing ```
                    code_lines = []
                    for k in range(j + 1, len(lines)):
                        if lines[k].startswith("```"):
                            return "\n".join(code_lines).strip()
                        code_lines.append(lines[k])
                    break
    # Fallback: heuristically return first code block
    return blocks[0].strip()


def show_diff_and_confirm(
    filename: Path, new_content: str, auto_yes: bool
) -> bool:
    """
    Show unified diff between existing and new content, ask user Y/N.
    Return True if the change should be applied.
    """
    if not filename.exists():
        print(f"\n👻  Creating new file: {filename}")
        print("=" * 72)
        print(new_content)
        print("=" * 72)
    else:
        old_lines = filename.read_text().splitlines(keepends=True)
        new_lines = [l + "\n" for l in new_content.splitlines()]
        diff_lines = list(
            difflib.unified_diff(
                old_lines, new_lines, fromfile=str(filename), tofile=str(filename)
            )
        )
        print(f"\n👻  Spectral changes to {filename}:")
        print("=" * 72)
        colour_diff(diff_lines if diff_lines else ["<no changes>\n"])
        print("=" * 72)

    if auto_yes:
        return True

    try:
        resp = input("Let the ghost make these changes? [y/N]: ")
    except EOFError:
        return False
    return resp.strip().lower().startswith("y")


def apply_code_changes(response: str, prompt: str, auto_yes: bool, force_code: bool = False) -> None:
    """
    If the prompt requested modifications, scan response for code blocks and
    apply them to referenced files with user approval.
    """
    if not (is_modification_request(prompt) or force_code):
        return

    referenced_files = FILE_REF_RE.findall(prompt)
    changes_applied = False

    for fname in referenced_files:
        path = Path(fname)
        code = extract_code_for_file(response, fname)
        if code:
            if show_diff_and_confirm(path, code, auto_yes):
                path.write_text(code)
                print(f"✅  GhostCoder manifested changes to {path}")
                changes_applied = True
        else:
            print(f"👻  No spectral code detected for {fname}")

    # If nothing matched but there is a generic block, just show it.
    if not changes_applied and not referenced_files:
        code = extract_code_for_file(response)
        if code:
            print("\n👻  GhostCoder materialized some code:")
            print("=" * 72)
            print(code)
            print("=" * 72)
            print("Hint: Use @filename in your prompt to let the ghost modify files")
        elif force_code:
            print("\n👻  No code blocks found in response. Consider:")
            print("   • Using @filename to reference specific files")
            print("   • Being more explicit about what code you want")
            print("   • Using the --force-code flag (already active)")


def send_prompt(prompt: str, auto_apply: bool, auto_yes: bool, force_code: bool = False) -> None:
    processed_prompt, has_refs, is_mod = process_file_references(prompt, force_code)
    
    # Construct the full prompt with system instructions
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser request: {processed_prompt}"
    
    try:
        r = requests.post(
            f"{BASE_URL}/api/generate",
            json={"model": MODEL, "prompt": full_prompt, "stream": False},
            timeout=180,
        )
        r.raise_for_status()
    except requests.RequestException as exc:
        sys.exit(f"👻  Cannot reach the spectral realm at {BASE_URL} : {exc}")

    try:
        ai_response = r.json().get("response")
    except ValueError as exc:
        sys.exit(f"👻  The ghost's voice faded… (invalid JSON): {exc}")

    if not ai_response:
        sys.exit("👻  Empty response from the ghost")

    print(ai_response)
    
    # Enhanced fallback: if no code blocks found but this was a modification request, 
    # try to extract any code-like content and show it
    if auto_apply:
        apply_code_changes(ai_response, prompt, auto_yes, force_code)
    elif is_mod and not CODE_BLOCK_RE.search(ai_response):
        print("\n👻  No code blocks detected in response. Attempting to extract code-like content...")
        # Look for code-like patterns that might not be in proper code blocks
        lines = ai_response.splitlines()
        code_lines = []
        in_code_section = False
        
        for line in lines:
            if any(indicator in line.lower() for indicator in ['def ', 'class ', 'import ', 'from ', 'if __name__', '#!/']):
                in_code_section = True
            if in_code_section and line.strip():
                code_lines.append(line)
            elif in_code_section and not line.strip() and code_lines:
                break
        
        if code_lines:
            print("\n👻  Found potential code content:")
            print("=" * 72)
            print("\n".join(code_lines))
            print("=" * 72)
            print("💡  Consider using @filename to let the ghost modify files directly")
        elif force_code:
            print("\n👻  No code blocks found despite force-code mode.")
            print("💡  Try being more specific about what code you want generated.")


# --------------------------------------------------------------------------- #
#  CLI / main                                                                  #
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ghostcoder",
        description="👻  GhostCoder ‑ your phantom coding assistant (Python edition)",
        add_help=False,
        epilog="""
Examples:
  ghostcoder "fix the bug in @main.py"
  ghostcoder --force-code "implement a login system"
  ghostcoder -y "add error handling to @utils.py"
  ghostcoder --no-apply "explain how this code works"
        """,
    )
    p.add_argument("-p", "--print", dest="print_only", action="store_true")
    p.add_argument("-y", "--yes", dest="auto_yes", action="store_true")
    p.add_argument("--no-apply", dest="no_apply", action="store_true")
    p.add_argument("--force-code", dest="force_code", action="store_true",
                   help="Force the ghost to return code changes instead of explanations")
    p.add_argument("-h", "--help", action="help")
    p.add_argument("prompt", nargs=argparse.REMAINDER, help="Prompt for the ghost")
    return p


def interactive_loop(auto_apply: bool, auto_yes: bool, force_code: bool = False) -> None:
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


def main(argv: List[str] = None) -> None:
    args = build_parser().parse_args(argv)
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

