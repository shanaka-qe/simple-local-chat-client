# Terminal Chatbot (LangChain + Ollama + optional LangSmith)

This is a simple, terminal-based chatbot that runs entirely on your machine using a local LLM served by Ollama. It keeps per-session chat history so the model answers with context. Optionally, you can enable LangSmith to trace and inspect your conversations for debugging/evaluation.

## What this project is
- A minimal Python project showing how to:
  - Use a local model via Ollama (default: `gemma3:4b`)
  - Build a conversational loop with LangChain’s modern Runnable + Message History API
  - Maintain conversation history across turns
  - Optionally enable LangSmith tracing

## Prerequisites
1) Install Python 3.10+
2) Install Ollama and pull a model
```bash
brew install ollama # macOS (or see ollama.ai for your OS)
ollama serve
ollama pull gemma3:4b
```

## Setup
```bash
# (Recommended) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create your environment file
cp .env.example .env
# Edit .env and set values as needed
```

`.env.example` values
```env
LANGSMITH_API_KEY=your_langsmith_api_key_here   # optional
LANGSMITH_PROJECT=langchain-chatbot            # optional
OLLAMA_MODEL=gemma3:4b                         # local model name in Ollama
# OLLAMA_BASE_URL=http://localhost:11434       # optional if non-default
```

## Run
```bash
python main.py
```

Commands inside the chat
- `clear`: reset conversation memory
- `memory`: print a short summary of recent messages
- `quit` / `exit`: leave the program

## How it works (high level)
- `src/llm_manager.py`: wraps the local Ollama model for LangChain
- `src/chatbot.py`: builds a chain with `RunnableWithMessageHistory` to maintain per-session history
- `config/settings.py`: reads environment variables and default settings
- `main.py`: CLI loop, optional LangSmith setup, and overall orchestration

## Codebase Architecture

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

## Troubleshooting
- “Model not available”: ensure `ollama serve` is running and the model exists (`ollama list`). Update `OLLAMA_MODEL` in `.env` if needed.
- “LangSmith API key not found”: tracing is optional; add `LANGSMITH_API_KEY` to `.env` to enable.
- Import errors: verify your virtual environment is active and run `pip install -r requirements.txt`.

## Privacy & publishing
- No secrets are hardcoded. Keep your `.env` private (already covered by `.gitignore`).
- The project runs your model locally; no prompts or responses are sent to remote LLMs unless you enable LangSmith tracing, which sends metadata to LangSmith.

## License
Educational example. Use and modify as you like.
