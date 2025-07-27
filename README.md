# 👻 GhostCoder (Python Edition)

A phantom developer that haunts your terminal, powered by a local Ollama server. Now with **enhanced agentic behavior** to ensure you get actual code changes instead of just explanations!

## ✨ New Features

### 🔧 `--force-code` Flag
Force the ghost to prioritize code generation over explanations:
```bash
ghostcoder --force-code "implement a user authentication system"
```

### 🧠 Enhanced System Prompt
The ghost now receives explicit instructions to:
- Always provide complete code in code blocks
- Focus on implementation over explanation
- Show actual code changes, not just descriptions

### 🎯 Improved Code Detection
- Better keyword detection for modification requests
- Enhanced fallback logic when no code blocks are found
- Automatic extraction of code-like content from responses

### 📝 Better Prompt Engineering
- More explicit instructions when modifying files
- Clearer guidance for the LLM on what type of response is expected
- Enhanced context when file references are used

## 🚀 Usage Examples

### Basic Usage
```bash
# Modify a specific file
ghostcoder "fix the bug in @main.py"

# Force code generation
ghostcoder --force-code "implement a login system"

# Auto-apply changes
ghostcoder -y "add error handling to @utils.py"

# Just explain (no code changes)
ghostcoder --no-apply "explain how this code works"
```

### Interactive Mode
```bash
ghostcoder
# Enter interactive séance mode
# Use @filename to reference files
# Type 'exit' to quit
```

## 🔧 Installation

1. Ensure you have Python 3.8+ and Ollama running
2. Install dependencies:
   ```bash
   pip install requests
   ```
3. Set environment variables (optional):
   ```bash
   export OLLAMA_BASE_URL="http://localhost:11434"
   export OLLAMA_MODEL="deepseek-coder:6.7b-instruct"
   ```

## 🎯 Key Improvements

### Before
- LLM sometimes gave explanations instead of code
- No way to force code generation
- Limited fallback when no code blocks found

### After
- **Agentic behavior**: LLM is explicitly instructed to provide code
- **Force-code mode**: Guaranteed code generation attempts
- **Smart fallbacks**: Extracts code-like content when blocks aren't found
- **Better prompts**: More explicit instructions for the model

## 🛠️ Technical Details

### Enhanced Prompt Engineering
The system now includes a comprehensive system prompt that instructs the LLM to:
- Always provide complete code in code blocks
- Focus on implementation over explanation
- Use proper code block syntax
- Be direct and actionable

### Improved Modification Detection
Added more keywords to detect modification requests:
- `write`, `generate`, `make`, `build`
- Better logic to distinguish explanations from modifications

### Fallback Mechanisms
When no code blocks are found:
1. Attempts to extract code-like patterns
2. Provides helpful suggestions
3. Shows potential code content when possible

## 📋 Requirements

- Python ≥3.8
- `requests` library
- Running Ollama server
- `colordiff` (optional, for colored diffs)

## 🎭 The Ghost's Personality

GhostCoder maintains its spooky theme while being more practical:
- 👻 Spectral changes and manifestations
- 🔮 Interactive séance mode
- 💀 Banish the ghost with 'exit'
- ✨ Magical code transformations

## 🤝 Contributing

Feel free to contribute improvements to make the ghost even more helpful!

---

*"The best code is the code that writes itself... with a little help from the ghost!"* 👻 