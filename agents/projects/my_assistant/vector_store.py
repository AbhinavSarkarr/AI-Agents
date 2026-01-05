import chromadb
from chromadb.utils import embedding_functions
import os
from typing import List, Dict, Any

class VectorStore:
    def __init__(self, db_path: str = "/home/jellyfish/Desktop/Agentic AI/chroma_db"):
        """Initialize ChromaDB vector store"""
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Use OpenAI embeddings
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-ada-002"
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(
                name="documents",
                embedding_function=openai_ef
            )
        except:
            self.collection = self.client.create_collection(
                name="documents",
                embedding_function=openai_ef
            )
    
    def add_document(self, text: str, metadata: Dict[str, Any] = None, doc_id: str = None):
        """Add a document to the vector store"""
        if doc_id is None:
            doc_id = f"doc_{hash(text)}"
        
        self.collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
    
    def add_documents(self, texts: List[str], metadatas: List[Dict[str, Any]] = None, ids: List[str] = None):
        """Add multiple documents to the vector store"""
        if ids is None:
            ids = [f"doc_{i}_{hash(text)}" for i, text in enumerate(texts)]
        
        if metadatas is None:
            metadatas = [{}] * len(texts)
        
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'id': results['ids'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        
        return formatted_results
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        try:
            count = self.collection.count()
            return {"document_count": count, "collection_name": "documents"}
        except Exception as e:
            return {"error": str(e), "document_count": 0}