#!/usr/bin/env python3
"""
AI client module for GhostCoder.
Handles communication with the Ollama API and response processing.
"""

import difflib
import sys
from pathlib import Path
from typing import List

try:
    import requests
except ImportError:
    sys.exit("❌  'requests' not found – run: pip install requests")

from config import BASE_URL, CODE_BLOCK_RE, FILE_REF_RE, MODEL, SYSTEM_PROMPT
from file_processor import extract_code_for_file, process_file_references
from utils import is_modification_request


def send_prompt(prompt: str, auto_apply: bool, auto_yes: bool, force_code: bool = False) -> None:
    """
    Send a prompt to the AI model and handle the response.
    
    Args:
        prompt: The user's prompt
        auto_apply: Whether to automatically apply code changes
        auto_yes: Whether to automatically confirm changes
        force_code: Whether to force code generation mode
    """
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


def apply_code_changes(response: str, prompt: str, auto_yes: bool, force_code: bool = False) -> None:
    """
    If the prompt requested modifications, scan response for code blocks and
    apply them to referenced files with user approval.
    
    Args:
        response: The AI model's response
        prompt: The original user prompt
        auto_yes: Whether to automatically confirm changes
        force_code: Whether to force code generation mode
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


def show_diff_and_confirm(filename: Path, new_content: str, auto_yes: bool) -> bool:
    """
    Show unified diff between existing and new content, ask user Y/N.
    Return True if the change should be applied.
    
    Args:
        filename: Path to the file being modified
        new_content: The new content to apply
        auto_yes: Whether to automatically confirm changes
        
    Returns:
        True if changes should be applied, False otherwise
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


def colour_diff(lines: List[str]) -> None:
    """
    Pretty‑print a unified diff, using colordiff if available.
    
    Args:
        lines: List of diff lines to display
    """
    import shutil
    import subprocess
    
    colordiff = shutil.which("colordiff")
    if colordiff:
        proc = subprocess.run(
            [colordiff, "-u", "-"], input="".join(lines).encode(), check=False
        )
        if proc.returncode in (0, 1):
            return
    # Fallback: plain text
    sys.stdout.writelines(lines) 