#!/usr/bin/env python3
"""
Setup module for GhostCoder.
Handles environment configuration and alias setup.
"""

import os
import sys
from pathlib import Path


def detect_shell() -> str:
    """
    Detect the user's shell.
    
    Returns:
        'zsh' or 'bash' based on the current shell
    """
    shell = os.environ.get('SHELL', '').lower()
    if 'zsh' in shell:
        return 'zsh'
    elif 'bash' in shell:
        return 'bash'
    else:
        # Default to zsh for macOS, bash for others
        return 'zsh' if sys.platform == 'darwin' else 'bash'


def get_rc_file_path(shell: str) -> Path:
    """
    Get the path to the shell RC file.
    
    Args:
        shell: The shell type ('zsh' or 'bash')
        
    Returns:
        Path to the RC file
    """
    home = Path.home()
    if shell == 'zsh':
        return home / '.zshrc'
    else:
        return home / '.bashrc'


def get_ghostcoder_path() -> Path:
    """
    Get the absolute path to the ghostcoder.py file.
    
    Returns:
        Absolute path to ghostcoder.py
    """
    # Get the directory where the current script is located
    script_dir = Path(__file__).parent.absolute()
    return script_dir / 'ghostcoder.py'


def add_to_rc_file(rc_path: Path, content: str) -> bool:
    """
    Add content to the RC file if it doesn't already exist.
    
    Args:
        rc_path: Path to the RC file
        content: Content to add
        
    Returns:
        True if content was added, False if it already existed
    """
    if not rc_path.exists():
        rc_path.touch()
    
    with open(rc_path, 'r') as f:
        existing_content = f.read()
    
    if content.strip() in existing_content:
        return False
    
    with open(rc_path, 'a') as f:
        f.write(f"\n# GhostCoder Configuration\n{content}\n")
    
    return True


def setup_environment() -> None:
    """
    Interactive setup for GhostCoder environment and aliases.
    """
    print("👻  GhostCoder Setup Wizard")
    print("=" * 50)
    
    # Detect shell
    shell = detect_shell()
    print(f"Detected shell: {shell}")
    
    # Get paths
    rc_path = get_rc_file_path(shell)
    ghostcoder_path = get_ghostcoder_path()
    
    print(f"RC file: {rc_path}")
    print(f"GhostCoder path: {ghostcoder_path}")
    print()
    
    # Environment variables setup
    print("🔧  Environment Variables Setup")
    print("-" * 30)
    
    current_base_url = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
    current_model = os.environ.get('OLLAMA_MODEL', 'deepseek-coder:6.7b-instruct')
    
    print(f"Current OLLAMA_BASE_URL: {current_base_url}")
    print(f"Current OLLAMA_MODEL: {current_model}")
    print()
    
    # Ask for custom values
    try:
        base_url = input(f"Enter OLLAMA_BASE_URL (press Enter for default '{current_base_url}'): ").strip()
        if not base_url:
            base_url = current_base_url
            
        model = input(f"Enter OLLAMA_MODEL (press Enter for default '{current_model}'): ").strip()
        if not model:
            model = current_model
    except KeyboardInterrupt:
        print("\n\n❌  Setup cancelled by user")
        return
    
    # Prepare environment variables content using string concatenation
    env_content = "export OLLAMA_BASE_URL=\"" + base_url + "\"\n"
    env_content += "export OLLAMA_MODEL=\"" + model + "\""
    
    # Prepare alias content using string concatenation
    alias_content = "alias ghost=\"python " + str(ghostcoder_path) + "\"\n"
    alias_content += "alias ghostcoder=\"ghost\""
    
    print()
    print("📝  Configuration Summary")
    print("-" * 25)
    print(f"Shell: {shell}")
    print(f"RC file: {rc_path}")
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")
    print(f"Alias: ghost -> python {ghostcoder_path}")
    print("Alias: ghostcoder -> ghost")
    print()
    
    # Ask for confirmation
    try:
        confirm = input("Apply these changes? [y/N]: ").strip().lower()
        if not confirm.startswith('y'):
            print("❌  Setup cancelled")
            return
    except KeyboardInterrupt:
        print("\n\n❌  Setup cancelled by user")
        return
    
    # Apply changes
    print()
    print("🔧  Applying changes...")
    
    # Add environment variables
    env_added = add_to_rc_file(rc_path, env_content)
    if env_added:
        print(f"✅  Added environment variables to {rc_path}")
    else:
        print(f"ℹ️   Environment variables already exist in {rc_path}")
    
    # Add aliases
    alias_added = add_to_rc_file(rc_path, alias_content)
    if alias_added:
        print(f"✅  Added aliases to {rc_path}")
    else:
        print(f"ℹ️   Aliases already exist in {rc_path}")
    
    print()
    print("🎉  Setup complete!")
    print()
    print("📋  Next steps:")
    print(f"1. Reload your shell: source {rc_path}")
    print("2. Test the setup: ghost --help")
    print("3. Start coding with GhostCoder!")
    print()
    print("💡  You can also restart your terminal to apply all changes.") 