# GhostCoder - Modular Python Edition

👻 A phantom developer that haunts your terminal, powered by a local Ollama server.

## Overview

This is a modular refactor of the original `ghostcoder.py` file, split into logical components for better maintainability and extensibility.

## Project Structure

```
GhostCoderV2/
├── main.py              # Main driver file (entry point)
├── config.py            # Configuration and constants
├── utils.py             # Utility functions
├── file_processor.py    # File handling and processing
├── ai_client.py         # AI/API communication
├── cli.py               # Command line interface
├── __init__.py          # Package initialization
├── ghostcoder.py        # Original monolithic file (preserved)
├── requirements.txt     # Dependencies
└── README_MODULAR.md    # This file
```

## Module Descriptions

### `main.py`
- **Purpose**: Main entry point and driver
- **Responsibilities**: 
  - Orchestrates the application flow
  - Handles command line argument processing
  - Manages interactive vs. single-shot modes

### `config.py`
- **Purpose**: Centralized configuration
- **Responsibilities**:
  - Environment variables (OLLAMA_BASE_URL, OLLAMA_MODEL)
  - Constants (MODIFICATION_WORDS, EXPLANATION_WORDS)
  - Regular expressions (CODE_BLOCK_RE, FILE_REF_RE)
  - System prompts

### `utils.py`
- **Purpose**: Utility functions
- **Responsibilities**:
  - Request type analysis (modification vs. explanation)
  - Helper functions for text processing

### `file_processor.py`
- **Purpose**: File handling and processing
- **Responsibilities**:
  - File reading operations
  - @filename reference processing
  - Code block extraction from AI responses

### `ai_client.py`
- **Purpose**: AI communication and response handling
- **Responsibilities**:
  - Ollama API communication
  - Response processing
  - Code change application
  - Diff generation and display

### `cli.py`
- **Purpose**: Command line interface
- **Responsibilities**:
  - Argument parsing
  - Interactive loop management
  - User input handling

## Usage

### Running the Application

```bash
# Run with a prompt
python main.py "fix the bug in @main.py"

# Interactive mode
python main.py

# Force code generation
python main.py --code "implement a login system"

# Auto-apply changes
python main.py --skip-confirm "add error handling to @utils.py"

# Print only (no file changes)
python main.py --no-apply "explain how this code works"
```

### As a Python Package

```python
from main import main

# Run with custom arguments
main(["fix", "the", "bug", "in", "@main.py"])
```

## Benefits of Modular Structure

1. **Maintainability**: Each module has a single responsibility
2. **Testability**: Individual components can be tested in isolation
3. **Extensibility**: Easy to add new features or modify existing ones
4. **Readability**: Code is organized logically and easier to understand
5. **Reusability**: Modules can be imported and used independently

## Migration from Original

The original `ghostcoder.py` file is preserved for reference. The new modular structure maintains 100% feature parity while providing better organization.

### Key Changes:
- **No functional changes**: All original features work exactly the same
- **Same CLI interface**: All command line options remain identical
- **Same behavior**: Interactive mode, file processing, and AI communication work identically
- **Better organization**: Code is now split into logical, focused modules

## Development

### Adding New Features

1. **Configuration**: Add constants to `config.py`
2. **Utilities**: Add helper functions to `utils.py`
3. **File Operations**: Add file-related functions to `file_processor.py`
4. **AI Features**: Add AI-related functionality to `ai_client.py`
5. **CLI Options**: Add new arguments to `cli.py`
6. **Integration**: Wire everything together in `main.py`

### Testing Individual Modules

```python
# Test file processing
from file_processor import process_file_references
result = process_file_references("fix @test.py", force_code=True)

# Test AI client
from ai_client import send_prompt
send_prompt("explain this code", auto_apply=False, auto_yes=False)

# Test utilities
from utils import is_modification_request
is_mod = is_modification_request("fix the bug")
```

## Dependencies

Same as the original:
- Python ≥3.8
- `requests` library
- `colordiff` (optional, for colored diffs)

## License

MIT - Same as the original project. 