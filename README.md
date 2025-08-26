# 👻 GhostCoder V2

**Your AI coding assistant that actually writes code, not just explanations!**

GhostCoder is a Python tool that connects to your local Ollama server to help you write, modify, and understand code. Unlike other AI assistants that often just explain things, GhostCoder is designed to **generate actual code** and **modify your files directly**.

## ⚡ Quick Start

### Prerequisites
- Python 3.8 or higher
- Ollama installed and running

### Setup (3 steps)
```bash
# 1. Create virtual environment
python3 -m venv venv && source venv/bin/activate

# 2. Install dependencies  
pip3 install -r requirements.txt

# 3. Run setup wizard
python ghostcoder.py --setup
```

**💡 Pro tip**: Always activate your virtual environment (`source venv/bin/activate`) before using GhostCoder!

## 🚀 Installation & Setup

### Option 1: Automatic Setup (Recommended)

The setup wizard automates everything:
```bash
python3 ghostcoder.py --setup
```

**What it does:**
- Detects your shell (zsh or bash)
- Configures environment variables
- Creates `ghost` and `ghostcoder` aliases
- Updates your shell RC file

### Option 2: Manual Setup

1. **Install Ollama** from [https://ollama.ai](https://ollama.ai)
2. **Pull a coding model**:
   ```bash
   ollama pull deepseek-coder:6.7b-instruct
   ```
3. **Set environment variables** in your `~/.zshrc` or `~/.bashrc`:
   ```bash
   export OLLAMA_BASE_URL="http://localhost:11434"
   export OLLAMA_MODEL="deepseek-coder:6.7b-instruct"
   ```
4. **Create an alias**:
   ```bash
   alias ghost="python /path/to/ghostcoder.py"
   ```

## 📖 Usage

### Basic Commands

```bash
# Generate code
ghost "create a web scraper"

# Modify a specific file
ghost "fix the bug in @main.py"

# Modify multiple files
ghost "add logging to @main.py @utils.py @config.py"

# Force code generation (recommended!)
ghost --code "implement user authentication"

# Auto-apply changes without asking
ghost --skip-confirm "add logging to @utils.py"

# Just get explanations (no code changes)
ghost --no-apply "explain how this function works"
```

### File Modifications

The `@filename` syntax lets you reference files for modification:

```bash
# Single file
ghost "add input validation to @app.py"

# Multiple files at once
ghost "add logging to @main.py @utils.py @config.py"
ghost "update error handling in @auth.py @user.py @middleware.py"
```

**Multifile Processing**: When you reference multiple files, GhostCoder processes each file individually with progress tracking and individual confirmations.

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
# Single file modifications
ghost "add error handling to @main.py"
ghost "optimize the algorithm in @utils.py"

# Multiple file modifications
ghost "add logging to @main.py @utils.py @config.py"
ghost "add type hints to @auth.py @user.py @middleware.py"
```

### Auto-apply with `--skip-confirm`
Skip the confirmation prompt:

```bash
ghost --skip-confirm "add comments to @script.py"
```

### Explanation Mode with `--no-apply`
When you only want explanations, not code changes:

```bash
ghost --no-apply "explain how this sorting algorithm works"
```

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

### Common Issues

#### "python: command not found"
- Use `python3` instead of `python` on macOS/Linux
- Make sure Python 3.8+ is installed: `python3 --version`

#### "externally-managed-environment" Error
- **Solution**: Always use a virtual environment:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

#### "Cannot reach the spectral realm"
- Make sure Ollama is running: `ollama serve`
- Check the URL: `curl http://localhost:11434`

#### "No code blocks detected"
- Use the `--code` flag: `ghost --code "your request"`
- Be more specific: `ghost --code "write a function that..."`

### Virtual Environment Best Practices
- **Always activate** your virtual environment before running GhostCoder
- **Never install packages globally** with pip
- **Keep your virtual environment** in the project directory

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