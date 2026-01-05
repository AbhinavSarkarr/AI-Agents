# AI Assistant with Vector Search

A smart chatbot that combines ChromaDB vector search with OpenAI's GPT models and tool calling capabilities.

## Features

- **Vector Search**: Uses ChromaDB to store and search through documents using semantic similarity
- **Tool Integration**: Supports multiple tools including:
  - User contact information recording
  - Unknown question logging
  - Knowledge base search
  - Push notifications via Pushover
- **RAG (Retrieval Augmented Generation)**: Enhances responses with relevant information from the knowledge base
- **Interactive UI**: Beautiful Gradio interface for easy interaction

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure your `.env` file has the required API keys:
- `OPENAI_API_KEY`: Your OpenAI API key
- `PUSHOVER_USER`: (Optional) Pushover user key for notifications
- `PUSHOVER_TOKEN`: (Optional) Pushover app token for notifications

3. The system will automatically use the existing ChromaDB database located at `/home/jellyfish/Desktop/Agentic AI/chroma_db`

## Usage

Run the chatbot:
```bash
python chatbot.py
```

This will:
1. Initialize the vector store with your existing ChromaDB
2. Add sample documents (if enabled)
3. Launch the Gradio interface on `http://localhost:7860`

## Components

### `vector_store.py`
- Handles ChromaDB operations
- Manages document storage and retrieval
- Provides semantic search functionality

### `tools.py`
- Defines available tools for the AI assistant
- Handles tool execution
- Manages push notifications

### `chatbot.py`
- Main application logic
- Integrates vector search with LLM responses
- Manages the conversation flow and tool calling

## How It Works

1. **User Input**: User sends a message through the Gradio interface
2. **Vector Search**: System searches the knowledge base for relevant information
3. **Context Enhancement**: Relevant documents are added to the conversation context
4. **LLM Processing**: OpenAI processes the request with enhanced context and available tools
5. **Tool Execution**: If the LLM decides to use tools, they are executed automatically
6. **Response**: Final response is generated and returned to the user

## Example Interactions

- Ask about topics in your knowledge base: "What do you know about AI in healthcare?"
- Provide contact information: "I'd like to get in touch - my email is user@example.com"
- Ask questions the system doesn't know: "What's the weather like today?" (will be logged)
- Technical queries: "How do vector databases work?"

## Notes

- The system uses `text-embedding-ada-002` for generating embeddings
- Pushover notifications require valid credentials in the `.env` file
- The vector store automatically connects to your existing ChromaDB database
- Sample documents are added on first run for demonstration purposes