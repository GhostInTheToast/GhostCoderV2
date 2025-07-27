# 👻 GhostCoder V2

**Your AI coding assistant that actually writes code, not just explanations!**

GhostCoder is a Python tool that connects to your local Ollama server to help you write, modify, and understand code. Unlike other AI assistants that often just explain things, GhostCoder is designed to **generate actual code** and **modify your files directly**.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install requests
```

### 2. Set up Ollama (if not already done)
```bash
# Install Ollama from https://ollama.ai
# Then pull a coding model:
ollama pull deepseek-coder:6.7b-instruct
```

### 3. Set up Environment Variables
```bash
# Add these to your ~/.zshrc or ~/.bashrc
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="deepseek-coder:6.7b-instruct"

# Reload your shell
source ~/.zshrc  # or source ~/.bashrc
```

### 4. Create an Alias (Optional but Recommended)
```bash
# Add this to your ~/.zshrc or ~/.bashrc
alias ghost="python /path/to/ghostcoder.py"

# Replace /path/to/ with the actual path to your ghostcoder.py file
# For example: alias ghost="python ~/Projects/ghostcoderV0.5/ghostcoder.py"

# Reload your shell
source ~/.zshrc  # or source ~/.bashrc
```

### 5. Use GhostCoder
```bash
# Basic usage (if you set up the alias)
ghost "create a function that calculates fibonacci numbers"

# Or run directly
python ghostcoder.py "create a function that calculates fibonacci numbers"

# Modify existing files
ghost "add error handling to @myfile.py"

# Force code generation (recommended!)
ghost --code "implement a login system"
```

## ✨ What Makes This Special?

### 🎯 **Actually Generates Code**
Most AI assistants just explain what to do. GhostCoder **writes the actual code** for you.

### 🔧 **Modifies Files Directly**
Use `@filename` to reference files, and GhostCoder will modify them with your approval.

### 🚀 **Smart Code Detection**
Automatically detects when you want code vs explanations, with a `--code` flag for guaranteed code generation.

## 📖 How to Use

### Basic Commands

```bash
# Generate code
ghost "create a web scraper"

# Modify a specific file
ghost "fix the bug in @main.py"

# Force code generation (recommended!)
ghost --code "implement user authentication"

# Auto-apply changes without asking
ghost -y "add logging to @utils.py"

# Just get explanations (no code changes)
ghost --no-apply "explain how this function works"
```

### File Modifications

The `@filename` syntax lets you reference files for modification:

```bash
# GhostCoder will read the file and modify it
ghost "add input validation to @app.py"

# Multiple files at once
ghost "update both @frontend.js and @backend.py"
```

### Interactive Mode

Run `ghost` without arguments to enter interactive mode:

```bash
ghost
# You: add a function to calculate square roots
# Ghost: [generates code]
# You: modify @math.py to use this function
# Ghost: [modifies the file]
# You: exit
```

## 🎯 Key Features

### `--code` Flag
**The most important feature!** Forces GhostCoder to generate actual code instead of explanations:

```bash
# Without --code (might just explain)
ghost "implement a calculator"

# With --code (guaranteed to generate code)
ghost --code "implement a calculator"
```

### File References with `@filename`
Reference any file in your project for modification:

```bash
ghost "add error handling to @main.py"
ghost "optimize the algorithm in @utils.py"
ghost "fix the bug in @config.json"
```

### Auto-apply with `-y`
Skip the confirmation prompt:

```bash
ghost -y "add comments to @script.py"
```

### Explanation Mode with `--no-apply`
When you only want explanations, not code changes:

```bash
ghost --no-apply "explain how this sorting algorithm works"
```

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- Ollama server running locally
- A coding model (like `deepseek-coder:6.7b-instruct`)

### Detailed Setup

1. **Install Python dependencies:**
   ```bash
   pip install requests
   ```

2. **Install and set up Ollama:**
   ```bash
   # Install from https://ollama.ai
   # Start Ollama server
   ollama serve
   
   # Pull a coding model
   ollama pull deepseek-coder:6.7b-instruct
   ```

3. **Download GhostCoder:**
   ```bash
   # Clone the repository
   git clone https://github.com/GhostInTheToast/GhostCoderV2.git
   cd GhostCoderV2
   
   # Or download the ghostcoder.py file directly
   ```

4. **Set up environment variables:**
   ```bash
   # Add to ~/.zshrc or ~/.bashrc
   export OLLAMA_BASE_URL="http://localhost:11434"
   export OLLAMA_MODEL="deepseek-coder:6.7b-instruct"
   
   # Reload your shell
   source ~/.zshrc  # or source ~/.bashrc
   ```

5. **Create an alias (recommended):**
   ```bash
   # Add to ~/.zshrc or ~/.bashrc
   alias ghost="python /full/path/to/ghostcoder.py"
   
   # Example:
   # alias ghost="python ~/Projects/ghostcoderV0.5/ghostcoder.py"
   
   # Reload your shell
   source ~/.zshrc  # or source ~/.bashrc
   ```

### Verify Installation
```bash
# Test if Ollama is running
curl http://localhost:11434

# Test GhostCoder
ghost --help
```

### Default Configuration
If you don't set environment variables, GhostCoder uses these defaults:
- `OLLAMA_BASE_URL`: `http://localhost:11434`
- `OLLAMA_MODEL`: `deepseek-coder:6.7b-instruct`

You can override these by setting the environment variables or by modifying the defaults in `ghostcoder.py`.

## 📝 Examples

### Example 1: Create New Code
```bash
ghost --code "create a function that validates email addresses"
```

**Output:**
```python
def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

### Example 2: Modify Existing File
```bash
ghost "add logging to @app.py"
```

**GhostCoder will:**
1. Read your `app.py` file
2. Show you the proposed changes
3. Ask for confirmation
4. Apply the changes if you approve

### Example 3: Interactive Session
```bash
ghost
# You: create a simple web server
# Ghost: [generates Flask server code]
# You: add error handling to it
# Ghost: [modifies the code with error handling]
# You: exit
```

## 🛠️ Troubleshooting

### "Cannot reach the spectral realm"
- Make sure Ollama is running: `ollama serve`
- Check the URL: `curl http://localhost:11434`

### "No code blocks detected"
- Use the `--code` flag: `ghost --code "your request"`
- Be more specific: `ghost --code "write a function that..."`

### "File not found"
- Make sure the file exists in your current directory
- Use the full path if needed: `ghost "modify @/path/to/file.py"`

## 🎭 The Ghost's Personality

GhostCoder maintains a fun, spooky theme:
- 👻 "Spectral changes" = file modifications
- 🔮 "Interactive séance" = interactive mode
- 💀 "Banish the ghost" = exit command
- ✨ "Manifested changes" = successful file updates

## 🤝 Contributing

Feel free to contribute improvements! The ghost is always learning new tricks.

---

**Happy coding with your spectral assistant!** 👻✨ 