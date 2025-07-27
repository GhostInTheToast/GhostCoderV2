#!/usr/bin/env python3
"""
Utility functions for GhostCoder.
Contains helper functions for request analysis and other utilities.
"""

from config import EXPLANATION_WORDS, MODIFICATION_WORDS


def is_modification_request(prompt: str) -> bool:
    """
    Determine if a prompt is requesting code modifications.
    
    Args:
        prompt: The user's prompt text
        
    Returns:
        True if the prompt requests modifications, False otherwise
    """
    lower = prompt.lower()
    if any(w in lower for w in EXPLANATION_WORDS):
        return False
    return any(w in lower for w in MODIFICATION_WORDS) 