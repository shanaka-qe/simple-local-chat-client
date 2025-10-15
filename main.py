"""
Main application for the LangChain Chatbot.
This script sets up LangSmith tracing and provides a command-line interface.
"""

import os
from langsmith import Client
from config.settings import LANGSMITH_API_KEY, LANGSMITH_PROJECT, validate_config
from src.llm_manager import LLMManager
from src.chatbot import Chatbot

def setup_langsmith():
    """
    Set up LangSmith tracing for monitoring LLM calls.
    This allows us to track and analyze all interactions with the language model.
    """
    # Check if LangSmith API key is available
    if not LANGSMITH_API_KEY:
        print("⚠️  LangSmith API key not found. Tracing will be disabled.")
        print("   To enable tracing, set LANGSMITH_API_KEY in your .env file.")
        return False
    
    try:
        # Initialize LangSmith client
        # This client will send trace data to LangSmith for monitoring
        client = Client(api_key=LANGSMITH_API_KEY)
        
        # Set the project name for organizing traces
        # All traces from this session will be grouped under this project
        os.environ["LANGCHAIN_PROJECT"] = LANGSMITH_PROJECT
        
        print(f"✓ LangSmith tracing enabled for project: {LANGSMITH_PROJECT}")
        return True
        
    except Exception as e:
        print(f"✗ Error setting up LangSmith: {e}")
        return False

def print_welcome():
    """
    Print a welcome message and instructions for the user.
    This helps users understand how to interact with the chatbot.
    """
    print("=" * 60)
    print("🤖 LangChain Chatbot with Ollama and LangSmith")
    print("=" * 60)
    print("Welcome! You can now chat with your local Llama model.")
    print("\nCommands:")
    print("  - Type your message and press Enter to chat")
    print("  - Type 'clear' to start a new conversation")
    print("  - Type 'memory' to see conversation history")
    print("  - Type 'quit' or 'exit' to end the session")
    print("=" * 60)

def main():
    """
    Main function that runs the chatbot application.
    This function handles initialization, setup, and the main chat loop.
    """
    # Validate configuration before starting
    # This checks if all required settings are present
    if not validate_config():
        print("❌ Configuration validation failed. Please check your .env file.")
        return
    
    # Set up LangSmith tracing
    # This enables monitoring of all LLM interactions
    langsmith_enabled = setup_langsmith()
    
    try:
        # Initialize the LLM manager
        # This sets up the connection to the local Ollama model
        print("🔄 Initializing LLM manager...")
        llm_manager = LLMManager()
        
        # Check if the model is available
        # This prevents errors if the model isn't installed or Ollama isn't running
        if not llm_manager.check_model_availability():
            print("❌ Model not available. Please check your Ollama installation.")
            print("   Make sure Ollama is running: ollama serve")
            print(f"   Install the model: ollama pull {llm_manager.model_name}")
            return
        
        # Initialize the chatbot
        # This creates the conversation chain with memory
        print("🔄 Initializing chatbot...")
        chatbot = Chatbot(llm_manager)
               
        # Print welcome message
        print_welcome()
        
        # Main chat loop
        # This is where the user interacts with the chatbot
        while True:
            try:
                # Get user input
                # This waits for the user to type a message
                user_input = input("\n👤 You: ").strip()
                
                # Handle special commands
                # These commands control the chatbot behavior
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'clear':
                    # Clear conversation memory
                    chatbot.clear_memory()
                    continue
                elif user_input.lower() == 'memory':
                    # Show conversation history
                    print("\n📝 " + chatbot.get_memory_summary())
                    continue
                elif not user_input:
                    print("💬 Please enter a message to continue the conversation.")
                    continue
                
                # Get chatbot response
                # This processes the user input and returns a response
                print("🤖 Bot: ", end="", flush=True)
                response = chatbot.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                # Handle any unexpected errors
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'quit' to exit.")
    
    except Exception as e:
        # Handle initialization errors
        print(f"❌ Failed to initialize chatbot: {e}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    """
    This ensures the main function only runs when the script is executed directly.
    It won't run if the script is imported as a module.
    """
    main()
