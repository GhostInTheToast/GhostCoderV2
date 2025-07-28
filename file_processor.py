#!/usr/bin/env python3
"""
File processing module for GhostCoder.
Handles file reading, file reference processing, and code extraction.
"""

from pathlib import Path
from typing import Tuple

from config import CODE_BLOCK_RE, FILE_REF_RE
from utils import is_modification_request


def read_file(path: Path) -> str:
    """
    Read a file and return its contents.
    
    Args:
        path: Path to the file to read
        
    Returns:
        File contents as string, or error message if file cannot be read
    """
    try:
        return path.read_text()
    except Exception as exc:
        return f"[Error reading {path}: {exc}]"


def process_file_references(prompt: str, force_code: bool = False) -> Tuple[str, bool, bool]:
    """
    Replace @filename tokens with embedded file blocks.

    Args:
        prompt: The original prompt text
        force_code: Whether to force code generation mode
        
    Returns:
        Tuple of (processed_prompt, has_file_refs, is_modification)
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
    
    Args:
        response: The AI model's response text
        filename: Optional filename to look for specific code blocks
        
    Returns:
        Extracted code as string, or empty string if no code found
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


def process_multiple_file_references(prompt: str, force_code: bool = False) -> list[tuple[Path, str, str]]:
    """
    Process multiple @filename references and return individual prompts for each file.
    
    Args:
        prompt: The original prompt text
        force_code: Whether to force code generation mode
        
    Returns:
        List of tuples: [(file_path, original_prompt, processed_prompt), ...]
        If no file references found, returns empty list
    """
    file_references = FILE_REF_RE.findall(prompt)
    if not file_references:
        return []
    
    results = []
    is_mod = is_modification_request(prompt) or force_code
    
    for filename in file_references:
        path = Path(filename)
        if not path.exists():
            print(f"⚠️   File '{filename}' not found, skipping...")
            continue
            
        # Create a focused prompt for this specific file
        # Remove all @filename references and replace with just this one
        clean_prompt = FILE_REF_RE.sub('', prompt).strip()
        file_prompt = f"{clean_prompt} in the file @{filename}"
        
        # Process this single file reference
        processed_prompt, has_refs, _ = process_file_references(file_prompt, force_code)
        
        results.append((path, prompt, processed_prompt))
    
    return results


def has_multiple_file_references(prompt: str) -> bool:
    """
    Check if the prompt contains multiple @filename references.
    
    Args:
        prompt: The prompt text to check
        
    Returns:
        True if multiple file references found, False otherwise
    """
    file_references = FILE_REF_RE.findall(prompt)
    return len(file_references) > 1 