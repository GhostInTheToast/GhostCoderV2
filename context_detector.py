#!/usr/bin/env python3
"""
Smart context detection module for GhostCoder.
Analyzes prompts to find relevant files without explicit @filename references.
"""

from pathlib import Path
from typing import Dict, List

# Domain-specific keywords that indicate file types or areas
DOMAIN_KEYWORDS = {
    # Web/API related
    'api': ['api', 'endpoint', 'route', 'controller', 'view'],
    'web': ['web', 'frontend', 'html', 'css', 'javascript', 'js', 'react', 'vue'],
    'database': ['database', 'db', 'model', 'schema', 'migration', 'query'],
    
    # Authentication/Security
    'auth': ['auth', 'authentication', 'login', 'logout', 'password', 'security', 'jwt', 'token'],
    'user': ['user', 'account', 'profile', 'registration'],
    'middleware': ['middleware', 'interceptor', 'filter'],
    
    # Application layers
    'config': ['config', 'configuration', 'settings', 'env', 'environment'],
    'utils': ['utils', 'utilities', 'helpers', 'common', 'shared'],
    'main': ['main', 'app', 'application', 'entry', 'startup'],
    'service': ['service', 'business', 'logic', 'core'],
    
    # File operations
    'file': ['file', 'upload', 'download', 'storage', 'io'],
    'logging': ['log', 'logging', 'debug', 'trace'],
    'error': ['error', 'exception', 'handling', 'try', 'catch'],
    
    # Testing
    'test': ['test', 'spec', 'unit', 'integration', 'fixture'],
    
    # Documentation
    'doc': ['doc', 'documentation', 'readme', 'comment'],
}

# File patterns that match different types of files
FILE_PATTERNS = {
    'python': r'\.py$',
    'javascript': r'\.(js|jsx|ts|tsx)$',
    'web': r'\.(html|css|scss|sass)$',
    'config': r'\.(json|yaml|yml|toml|ini|cfg|conf)$',
    'documentation': r'\.(md|txt|rst)$',
    'test': r'(test|spec|_test|_spec)\.',
}

def analyze_prompt_intent(prompt: str) -> Dict[str, float]:
    """
    Analyze a prompt to determine the intent and relevant domains.
    
    Args:
        prompt: The user's prompt text
        
    Returns:
        Dictionary mapping domain keywords to relevance scores (0.0 to 1.0)
    """
    prompt_lower = prompt.lower()
    scores = {}
    
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = 0.0
        for keyword in keywords:
            if keyword in prompt_lower:
                score += 1.0
        if score > 0:
            scores[domain] = min(score / len(keywords), 1.0)
    
    return scores

def find_relevant_files(project_path: Path, intent_scores: Dict[str, float], 
                       max_files: int = 10) -> List[Path]:
    """
    Find files relevant to the detected intent.
    
    Args:
        project_path: Path to the project root
        intent_scores: Dictionary of domain scores from analyze_prompt_intent
        max_files: Maximum number of files to return
        
    Returns:
        List of relevant file paths, sorted by relevance
    """
    if not intent_scores:
        return []
    
    relevant_files = []
    
    # Get all Python files in the project, excluding virtual environments and hidden directories
    python_files = []
    for py_file in project_path.rglob("*.py"):
        # Skip virtual environments and hidden directories
        if any(part.startswith('.') for part in py_file.parts):
            continue
        if any(part in ['venv', 'env', 'ghost', '__pycache__', 'node_modules', 'site-packages'] for part in py_file.parts):
            continue
        # Only include files in the current project directory (not subdirectories of virtual envs)
        if 'ghost' in py_file.parts and py_file.parts.index('ghost') < len(py_file.parts) - 1:
            continue
        python_files.append(py_file)
    
    for file_path in python_files:
        relevance_score = calculate_file_relevance(file_path, intent_scores)
        if relevance_score > 0.1:  # Minimum relevance threshold
            relevant_files.append((file_path, relevance_score))
    
    # Sort by relevance score (highest first)
    relevant_files.sort(key=lambda x: x[1], reverse=True)
    
    # Return top files up to max_files
    return [file_path for file_path, score in relevant_files[:max_files]]

def calculate_file_relevance(file_path: Path, intent_scores: Dict[str, float]) -> float:
    """
    Calculate how relevant a file is to the detected intent.
    
    Args:
        file_path: Path to the file to analyze
        intent_scores: Dictionary of domain scores
        
    Returns:
        Relevance score between 0.0 and 1.0
    """
    if not file_path.exists():
        return 0.0
    
    try:
        content = file_path.read_text().lower()
        filename = file_path.name.lower()
        stem = file_path.stem.lower()
        
        total_score = 0.0
        
        # Check filename relevance
        for domain, keywords in DOMAIN_KEYWORDS.items():
            if domain in intent_scores:
                domain_score = intent_scores[domain]
                for keyword in keywords:
                    if keyword in filename or keyword in stem:
                        total_score += domain_score * 0.5  # Filename matches are weighted
                        break
        
        # Check content relevance
        for domain, keywords in DOMAIN_KEYWORDS.items():
            if domain in intent_scores:
                domain_score = intent_scores[domain]
                keyword_matches = sum(1 for keyword in keywords if keyword in content)
                if keyword_matches > 0:
                    total_score += domain_score * (keyword_matches / len(keywords)) * 0.3
        
        # Check for common patterns
        if any(pattern in filename for pattern in ['main', 'app', 'core']):
            total_score += 0.2  # Main application files get bonus
        
        return min(total_score, 1.0)
        
    except Exception:
        return 0.0

def detect_context_files(prompt: str, project_path: Path = None) -> List[Path]:
    """
    Main function to detect relevant files based on prompt context.
    
    Args:
        prompt: The user's prompt text
        project_path: Path to the project root (defaults to current directory)
        
    Returns:
        List of relevant file paths
    """
    if project_path is None:
        project_path = Path.cwd()
    
    # Analyze the prompt intent
    intent_scores = analyze_prompt_intent(prompt)
    
    if not intent_scores:
        return []
    
    # Find relevant files
    relevant_files = find_relevant_files(project_path, intent_scores)
    
    return relevant_files

def format_context_summary(prompt: str, detected_files: List[Path]) -> str:
    """
    Format a summary of the detected context for user feedback.
    
    Args:
        prompt: The original user prompt
        detected_files: List of detected relevant files
        
    Returns:
        Formatted summary string
    """
    if not detected_files:
        return "👻  No relevant files detected for this request."
    
    summary = f"👻  Smart context detection found {len(detected_files)} relevant file(s):\n"
    
    for i, file_path in enumerate(detected_files, 1):
        summary += f"   {i}. {file_path.name}\n"
    
    summary += f"\n💡  Processing: {prompt}"
    
    return summary