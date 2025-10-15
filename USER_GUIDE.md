# Simple Local Chat Client - User Guide

A comprehensive step-by-step guide to set up and use the terminal-based chatbot on your local machine.

## Table of Contents
1. [What You'll Need](#what-youll-need)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Using the Chat Interface](#using-the-chat-interface)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Configuration](#advanced-configuration)

## What You'll Need

Before starting, ensure you have:
- **Python 3.10 or higher** installed on your system
- **Ollama** installed and running
- **Git** (optional, for cloning the repository)
- **Terminal/Command Prompt** access

### Checking Your Python Version
```bash
python --version
# or
python3 --version
```

If you don't have Python 3.10+, visit [python.org](https://python.org) to download and install it.

## Installation Steps

### Step 1: Get the Project Files

**Option A: Clone with Git (Recommended)**
```bash
git clone <repository-url>
cd simple-local-chat-client
```

**Option B: Download as ZIP**
1. Download the project as a ZIP file
2. Extract it to your desired location
3. Open terminal in the project folder

### Step 2: Install Ollama

**For macOS:**
```bash
# Install using Homebrew
brew install ollama

# Start Ollama service
ollama serve
```

**For Windows:**
1. Download Ollama from [ollama.ai](https://ollama.ai)
2. Install the downloaded file
3. Open Command Prompt and run: `ollama serve`

**For Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
```

### Step 3: Download a Language Model

In a new terminal window (keep Ollama running in the first one):
```bash
# Download the default model (about 2.4GB)
ollama pull gemma3:4b

# Alternative models you can try:
# ollama pull llama3.2:3b    # Smaller, faster
# ollama pull llama3.2:8b    # Larger, more capable
```

### Step 4: Set Up Python Environment

**Create a virtual environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

**Install required packages:**
```bash
pip install -r requirements.txt
```

## Configuration

### Step 1: Create Environment File

```bash
# Copy the example environment file
cp .env.example .env
```

### Step 2: Edit Environment Variables

Open `.env` file in a text editor and configure:

```env
# Required: Model name (must match what you downloaded with Ollama)
OLLAMA_MODEL=gemma3:4b

# Optional: LangSmith for conversation tracing
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=langchain-chatbot

# Optional: Custom Ollama server URL (if not running on localhost:11434)
# OLLAMA_BASE_URL=http://localhost:11434
```

**Important Notes:**
- `OLLAMA_MODEL` must match the model you downloaded with `ollama pull`
- LangSmith settings are optional - leave blank if you don't have an account
- Don't share your `.env` file - it's already in `.gitignore`

## Running the Application

### Step 1: Ensure Ollama is Running

In one terminal window:
```bash
ollama serve
```

You should see output like:
```
time=2024-01-01T12:00:00.000Z level=INFO source=images.go:123 msg="total blobs: 1"
time=2024-01-01T12:00:00.000Z level=INFO source=images.go:130 msg="total unused blobs removed: 0"
time=2024-01-01T12:00:00.000Z level=INFO source=routes.go:1004 msg="Listening on 127.0.0.1:11434"
```

### Step 2: Start the Chat Application

In another terminal window:
```bash
# Navigate to project directory
cd simple-local-chat-client

# Activate virtual environment (if not already active)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Run the application
python main.py
```

You should see:
```
🤖 Simple Local Chat Client
Type 'quit' or 'exit' to end the conversation.
Type 'clear' to reset conversation memory.
Type 'memory' to see recent conversation summary.

You: 
```

## Using the Chat Interface

### Basic Usage

1. **Start chatting:** Simply type your message and press Enter
2. **Get help:** Type `help` to see available commands
3. **Clear memory:** Type `clear` to reset the conversation
4. **View memory:** Type `memory` to see a summary of recent messages
5. **Exit:** Type `quit` or `exit` to close the application

### Available Commands

| Command | Description |
|---------|-------------|
| `clear` | Reset conversation memory and start fresh |
| `memory` | Show a summary of recent conversation |
| `quit` or `exit` | Close the application |
| `help` | Show available commands |

### Example Conversation

```
You: Hello! Can you help me write a Python function?

🤖 Hello! I'd be happy to help you write a Python function. What kind of function are you looking to create? For example:
- A function to calculate something
- A function to process data
- A function to interact with files
- Something else entirely

Please let me know what the function should do, and I'll help you write it!

You: A function to calculate the factorial of a number

🤖 Here's a Python function to calculate the factorial of a number:

```python
def factorial(n):
    """
    Calculate the factorial of a number.
    
    Args:
        n (int): The number to calculate factorial for
        
    Returns:
        int: The factorial of n
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

# Example usage:
print(factorial(5))  # Output: 120
print(factorial(0))  # Output: 1
```

This function uses recursion to calculate the factorial. The factorial of a number n is the product of all positive integers less than or equal to n.

You: quit
```

## Troubleshooting

### Common Issues and Solutions

**1. "Model not available" error**
- **Problem:** Ollama can't find the specified model
- **Solution:** 
  ```bash
  # Check available models
  ollama list
  
  # Pull the model if missing
  ollama pull gemma3:4b
  
  # Update .env file with correct model name
  ```

**2. "Connection refused" error**
- **Problem:** Ollama server isn't running
- **Solution:** 
  ```bash
  # Start Ollama in a separate terminal
  ollama serve
  ```

**3. "Import errors" when running**
- **Problem:** Python packages not installed
- **Solution:**
  ```bash
  # Ensure virtual environment is active
  source venv/bin/activate  # macOS/Linux
  venv\Scripts\activate     # Windows
  
  # Reinstall packages
  pip install -r requirements.txt
  ```

**4. "LangSmith API key not found" warning**
- **Problem:** Optional LangSmith tracing not configured
- **Solution:** This is just a warning - the app works without it. To enable:
  - Sign up at [langsmith.com](https://langsmith.com)
  - Get your API key
  - Add it to your `.env` file

**5. Slow responses**
- **Problem:** Model is too large for your system
- **Solution:** Try a smaller model:
  ```bash
  ollama pull llama3.2:3b
  # Update OLLAMA_MODEL in .env to llama3.2:3b
  ```

### Getting Help

If you're still having issues:
1. Check that all services are running (`ollama serve`)
2. Verify your `.env` file has the correct model name
3. Ensure your virtual environment is activated
4. Try restarting both Ollama and the chat application

## Advanced Configuration

### Using Different Models

You can use any Ollama-compatible model:

```bash
# List available models
ollama list

# Pull a different model
ollama pull llama3.2:8b
ollama pull codellama:7b
ollama pull mistral:7b

# Update .env file
OLLAMA_MODEL=llama3.2:8b
```

### Custom Ollama Server

If running Ollama on a different machine or port:

```env
OLLAMA_BASE_URL=http://your-server:11434
```

### LangSmith Integration

For conversation tracing and debugging:

1. Sign up at [langsmith.com](https://langsmith.com)
2. Create a new project
3. Get your API key
4. Update `.env`:
   ```env
   LANGSMITH_API_KEY=your_actual_api_key
   LANGSMITH_PROJECT=your_project_name
   ```

### Performance Optimization

**For faster responses:**
- Use smaller models (3B parameters)
- Close other applications
- Ensure sufficient RAM (4GB+ recommended)

**For better quality:**
- Use larger models (8B+ parameters)
- Ensure sufficient RAM (8GB+ recommended)

---

## Quick Start Summary

1. Install Ollama and run `ollama serve`
2. Pull a model: `ollama pull gemma3:4b`
3. Set up Python environment and install packages
4. Copy `.env.example` to `.env` and configure
5. Run `python main.py`
6. Start chatting!

**Need help?** Check the troubleshooting section above or refer to the main README.md for technical details.
