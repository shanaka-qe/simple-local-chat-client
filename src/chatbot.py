"""
Chatbot implementation using LangChain with conversation memory.
This module handles the conversation logic and maintains context across messages.
"""
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableLambda
from config.settings import MAX_MEMORY_SIZE, SYSTEM_MESSAGE

class Chatbot:
    """
    A conversational chatbot that maintains context across multiple messages.
    This class handles the conversation flow and memory management.
    """
    
    def __init__(self, llm_manager):
        """
        Initialize the Chatbot with a language model manager.
        
        Args:
            llm_manager (LLMManager): The LLM manager that provides the language model
        """
        # Store the LLM manager for accessing the language model
        self.llm_manager = llm_manager
        
        # Get the LangChain LLM object from the manager
        self.llm = llm_manager.get_llm()
        
        # Create conversation memory to maintain context using modern history API
        # Keep per-session histories in an in-memory store
        self._memory_store = {}
        
        # Create the conversation chain (LLM + prompt) wrapped with message history
        self.conversation_chain = self._create_conversation_chain()
        
        # Build a simple chained post-processor: take the draft answer from
        # the conversation chain and ask the model to format it concisely.
        format_prompt = ChatPromptTemplate.from_messages([
            ("system", "Rewrite the following assistant draft into a concise, helpful answer. Use short paragraphs and bullet points when listing steps or options."),
            ("human", "{draft}")
        ])

        # Map the output of the conversation chain into {draft}, then run the formatter prompt through the same LLM
        self.formatted_chain = {"draft": self.conversation_chain} | format_prompt | self.llm
    

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """
        Retrieve or create a chat history object for a given session id.
        """
        history = self._memory_store.get(session_id)
        if history is None:
            history = ChatMessageHistory()
            self._memory_store[session_id] = history
        return history
    

    def chat(self, user_input):
        """
        Process user input and return the chatbot's response.
        This is the main method for interacting with the chatbot.
        
        Args:
            user_input (str): The user's message
            
        Returns:
            str: The chatbot's response
        """
        try:
            # Use the chained runnable: generate draft with history -> format it
            response = self.formatted_chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": "default"}}
            )
            return getattr(response, "content", response)
        except Exception as e:
            # Return a helpful error message if something goes wrong
            return f"Sorry, I encountered an error: {e}"
    
    def clear_memory(self):
        """
        Clear the conversation memory.
        This starts a fresh conversation without any previous context.
        """
        # Clear the in-memory histories
        self._memory_store.clear()
        print("Conversation memory cleared. Starting fresh conversation.")
    
    def get_memory_summary(self):
        """
        Get a summary of the current conversation memory.
        This is useful for debugging and understanding what the chatbot remembers.
        
        Returns:
            str: Summary of the conversation history
        """
        # Get the conversation history from memory
        history = self.get_session_history("default")
        messages = getattr(history, "messages", [])

        if not messages:
            return "No conversation history yet."
        
        # Format the conversation history for display
        summary = "Recent conversation:\n"
        for i, message in enumerate(messages[-6:], 1):  # Show last 6 messages
            role = "Human" if isinstance(message, HumanMessage) else "AI"
            content = message.content[:100] + "..." if hasattr(message, "content") and len(message.content) > 100 else getattr(message, "content", "")
            summary += f"{i}. {role}: {content}\n"
        
        return summary
    
    def _clean_input(self, data):
        # Remove extra spaces, check if empty
        text = data.get("input", "").strip()
        if not text:
            return {"input": "Hello, how can I help you?"}
        return {"input": text}

    def _create_conversation_chain(self):
        """
        Create the LangChain runnable chain with message history.
        Combines the LLM, a chat prompt, and per-session history.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_MESSAGE),
            ("placeholder", "{chat_history}"),
            ("human", "{input}")
        ])

        core_chain = RunnableLambda(self._clean_input) | prompt | self.llm

        runnable_with_history = RunnableWithMessageHistory(
            core_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        return runnable_with_history
        