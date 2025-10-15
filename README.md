# Terminal Chatbot (LangChain + Ollama + optional LangSmith)

**Author:** Shanaka Fernando  
**LinkedIn:** https://www.linkedin.com/in/shanaka-qe/

This is a simple, terminal-based chatbot that runs entirely on your machine using a local LLM served by Ollama. It keeps per-session chat history so the model answers with context. Optionally, you can enable LangSmith to trace and inspect your conversations for debugging/evaluation.

## 🚀 Quick Start

**New to this project?** Start with our comprehensive [User Guide](USER_GUIDE.md) for step-by-step setup instructions.

**Already familiar?** Jump to the [Technical Details](#technical-details) below.

## What this project is
- A minimal Python project demonstrating:
  - Local model integration via Ollama (default: `gemma3:4b`)
  - LangChain's modern Runnable + Message History API
  - Per-session conversation history
  - Optional LangSmith tracing for debugging

## Prerequisites
- Python 3.10+
- Ollama installed and running
- A compatible language model downloaded

## Quick Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings

# 3. Run the application
python main.py
```

**Need detailed instructions?** See the [User Guide](USER_GUIDE.md) for complete setup steps, troubleshooting, and usage examples.

## Technical Details

### How it works (high level)
- `src/llm_manager.py`: wraps the local Ollama model for LangChain
- `src/chatbot.py`: builds a chain with `RunnableWithMessageHistory` to maintain per-session history
- `config/settings.py`: reads environment variables and default settings
- `main.py`: CLI loop, optional LangSmith setup, and overall orchestration

### Codebase Architecture

This diagram illustrates how the different parts of the application work together.

```ascii
+--------------------------------+
|           .env File            |
| (OLLAMA_MODEL, LANGSMITH_KEY)  |
+--------------------------------+
             |
             v
+--------------------------------+
|      config/settings.py        |
| (Loads .env, provides config)  |
+--------------------------------+
             |
             v
+------------------------------------------------------------------+
|                             main.py                              |
|------------------------------------------------------------------|
| - Initializes `LLMManager` and `Chatbot`                         |
| - Main chat loop (reads user input)                              |
| - Handles commands (`clear`, `memory`, `quit`)                   |
| - Calls `chatbot.chat(input)`                                    |
| - Optionally initializes LangSmith tracing                       |
+------------------------------------------------------------------+
             |
             | Calls
             v
+------------------------------------------------------------------+
|                           src/chatbot.py                           |
|------------------------------------------------------------------|
| - `Chatbot` class with `RunnableWithMessageHistory`              |
| - Manages conversation history (`_memory_store`)                 |
| - Creates prompt from system message, history, and user input    |
| - Invokes the LLM chain                                          |
+------------------------------------------------------------------+
             |
             | Uses LLM object from
             v
+------------------------------------------------------------------+
|                         src/llm_manager.py                         |
|------------------------------------------------------------------|
| - `LLMManager` class wraps `langchain_ollama.OllamaLLM`          |
| - Configures the LLM (model name, temperature, etc.)             |
| - Communicates with the Ollama server                            |
+------------------------------------------------------------------+
             |
             | HTTP API Calls
             v
+------------------------------------------------------------------+
|                          Ollama Server                           |
|------------------------------------------------------------------|
| - Runs as a separate local process                               |
| - Serves the specified LLM (e.g., `gemma3:4b`)                   |
+------------------------------------------------------------------+
```

### Environment Configuration

`.env.example` values:
```env
LANGSMITH_API_KEY=your_langsmith_api_key_here   # optional
LANGSMITH_PROJECT=langchain-chatbot            # optional
OLLAMA_MODEL=gemma3:4b                         # local model name in Ollama
# OLLAMA_BASE_URL=http://localhost:11434       # optional if non-default
```

### Chat Commands
- `clear`: reset conversation memory
- `memory`: print a short summary of recent messages
- `quit` / `exit`: leave the program

## Privacy & Security
- No secrets are hardcoded. Keep your `.env` private (already covered by `.gitignore`)
- The project runs your model locally; no prompts or responses are sent to remote LLMs unless you enable LangSmith tracing, which sends metadata to LangSmith

## License
Educational example. Use and modify as you like.