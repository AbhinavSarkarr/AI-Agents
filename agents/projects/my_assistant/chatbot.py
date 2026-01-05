import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from gradio import ChatInterface
import gradio as gr
from vector_store import VectorStore
from tools import TOOLS, handle_tool_calls
from pydantic import BaseModel
from typing import List

# Load environment variables
load_dotenv(override=True)

class ChatBot:
    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Initialize vector store
        self.vector_store = VectorStore()
        
        # Get vector store info
        info = self.vector_store.get_collection_info()
        print(f"Vector store initialized with {info.get('document_count', 0)} documents")
        
        # System prompt for the assistant
        self.system_prompt = """You are an intelligent AI assistant with access to a knowledge base and various tools. 

Your responsibilities:
1. Answer user questions using information from your knowledge base when relevant
2. If you don't know something, always use the record_unknown_question tool to log it
3. If a user shows interest in getting in touch or provides contact information, use the record_user_details tool
4. Use the search_knowledge_base tool to find relevant information from your vector database
5. Be professional, helpful, and engaging

Guidelines:
- Always search the knowledge base first when answering factual questions
- Be honest when you don't know something
- Try to steer conversations towards helping users get the information they need
- If users want to be contacted or provide an email, record their details
"""

    def search_and_enhance_context(self, message: str) -> str:
        """Search vector store and enhance context for the response"""
        try:
            # Search for relevant documents
            search_results = self.vector_store.search(message, n_results=3)
            
            if search_results and search_results[0]['distance'] < 0.3:  # Only use if relevant
                context = "\n\n## Relevant Information from Knowledge Base:\n"
                for i, result in enumerate(search_results, 1):
                    context += f"{i}. {result['document'][:500]}...\n"
                
                enhanced_prompt = self.system_prompt + context
                return enhanced_prompt
        except Exception as e:
            print(f"Search error: {e}")
        
        return self.system_prompt

    def chat(self, message: str, history: List) -> str:
        """Main chat function with tool calling support"""
        try:
            # Enhance system prompt with relevant context
            enhanced_system_prompt = self.search_and_enhance_context(message)
            
            # Prepare messages
            messages = [{"role": "system", "content": enhanced_system_prompt}]
            
            # Add conversation history
            for h in history:
                if isinstance(h, dict):
                    messages.append({"role": h["role"], "content": h["content"]})
                else:
                    # Handle Gradio's format
                    messages.append({"role": "user", "content": h[0]})
                    messages.append({"role": "assistant", "content": h[1]})
            
            # Add current user message
            messages.append({"role": "user", "content": message})
            
            # Continue calling the LLM until no more tool calls are needed
            done = False
            max_iterations = 5
            iteration = 0
            
            while not done and iteration < max_iterations:
                iteration += 1
                
                # Call OpenAI API with tools
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    tools=TOOLS,
                    temperature=0.7
                )
                
                finish_reason = response.choices[0].finish_reason
                
                if finish_reason == "tool_calls":
                    # Handle tool calls
                    message_with_tools = response.choices[0].message
                    tool_calls = message_with_tools.tool_calls
                    
                    # Execute tools
                    tool_results = handle_tool_calls(tool_calls, self.vector_store)
                    
                    # Add assistant message and tool results to conversation
                    messages.append(message_with_tools)
                    messages.extend(tool_results)
                else:
                    done = True
            
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            return f"I encountered an error while processing your request: {str(e)}"

    def add_sample_documents(self):
        """Add some sample documents to the vector store for testing"""
        sample_docs = [
            {
                "text": "Artificial Intelligence (AI) is transforming healthcare through diagnostic imaging, drug discovery, and personalized treatment plans. AI algorithms can analyze medical images with high accuracy, often surpassing human radiologists in detecting certain conditions.",
                "metadata": {"topic": "AI in Healthcare", "type": "overview"}
            },
            {
                "text": "Machine Learning models require large amounts of data for training. The quality and diversity of training data directly impacts model performance. Data preprocessing, feature engineering, and proper validation techniques are crucial for successful ML implementations.",
                "metadata": {"topic": "Machine Learning", "type": "technical"}
            },
            {
                "text": "Vector databases like ChromaDB enable semantic search by storing high-dimensional embeddings. These databases allow for similarity-based retrieval, making them perfect for RAG (Retrieval Augmented Generation) applications in AI systems.",
                "metadata": {"topic": "Vector Databases", "type": "technical"}
            },
            {
                "text": "Natural Language Processing (NLP) has evolved significantly with transformer models. BERT, GPT, and other large language models have revolutionized how machines understand and generate human language.",
                "metadata": {"topic": "NLP", "type": "overview"}
            }
        ]
        
        try:
            texts = [doc["text"] for doc in sample_docs]
            metadatas = [doc["metadata"] for doc in sample_docs]
            ids = [f"sample_{i}" for i in range(len(texts))]
            
            self.vector_store.add_documents(texts, metadatas, ids)
            print(f"Added {len(texts)} sample documents to the vector store")
            return True
        except Exception as e:
            print(f"Error adding sample documents: {e}")
            return False

    def launch(self, add_samples: bool = True):
        """Launch the Gradio interface"""
        if add_samples:
            self.add_sample_documents()
        
        # Create Gradio interface
        interface = ChatInterface(
            self.chat,
            type="messages",
            title="🤖 AI Assistant with Vector Search",
            description="Chat with an AI assistant that has access to a knowledge base and various tools.",
            examples=[
                "What do you know about AI in healthcare?",
                "Tell me about machine learning data requirements",
                "How do vector databases work?",
                "What is NLP?",
                "I'd like to get in touch - my email is user@example.com"
            ],
            retry_btn="🔄 Retry",
            undo_btn="↩️ Undo",
            clear_btn="🗑️ Clear",
        )
        
        return interface

def main():
    """Main function to run the chatbot"""
    print("Starting AI Assistant with Vector Search...")
    
    # Create chatbot instance
    bot = ChatBot()
    
    # Launch the interface
    interface = bot.launch(add_samples=True)
    
    # Start the interface
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )

if __name__ == "__main__":
    main()