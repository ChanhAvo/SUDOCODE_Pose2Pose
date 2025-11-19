"""
Backend functions for Streamlit frontend integration.

This module provides high-level functions that the frontend can call
to interact with the RAG system and other backend services.

Uses singleton pattern to ensure RAG components are initialized once
and reused throughout the application lifecycle.
"""

from typing import Any, Optional

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from backend.config import config
from backend.core.chromadb import ChromaVectorDB
from backend.core.rag import RAGSystem
from backend.core.video_service import get_video_service


class RAGServiceSingleton:
    """
    Singleton class for RAG service components.

    Ensures that embeddings, vector DB, LLM, and RAG system are initialized
    only once and reused throughout the application lifecycle.
    """

    _instance: Optional["RAGServiceSingleton"] = None
    _initialized: bool = False

    def __new__(cls) -> "RAGServiceSingleton":
        """Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize components only once."""
        # Skip if already initialized
        if RAGServiceSingleton._initialized:
            return

        # Initialize embeddings (reused for all operations)
        self.embeddings = OpenAIEmbeddings(
            model=config.openai_embedding_model,
            api_key=config.openai_api_key,
        )

        # Initialize vector database (persistent connection)
        self.vector_db = ChromaVectorDB(
            api_key=config.chroma_api_key,
            tenant=config.chroma_tenant,
            database=config.chroma_database,
            collection_name=config.chroma_collection_name,
            embedding_function=self.embeddings,
            distance_metric=config.chroma_distance_metric,
        )

        # Initialize LLM (reused for all generations)
        self.llm = ChatOpenAI(
            model=config.openai_model,
            temperature=0.1,
            api_key=config.openai_api_key,
        )

        # Create and build RAG system (chain built once)
        self.rag_system = RAGSystem(
            vector_db=self.vector_db,
            llm=self.llm,
        )
        self.rag_system.build_chain()

        # Mark as initialized
        RAGServiceSingleton._initialized = True

    @classmethod
    def get_instance(cls) -> "RAGServiceSingleton":
        """
        Get the singleton instance.

        Returns:
            RAGServiceSingleton: The singleton instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """
        Reset the singleton instance.

        Use this to force re-initialization, for example if config changes.
        """
        cls._instance = None
        cls._initialized = False


def query_rag_system(
    question: str,
    include_sources: bool = True,
    top_k: int = 3,
) -> dict[str, Any]:
    try:
        # Get singleton instance (initializes once, reuses thereafter)
        service = RAGServiceSingleton.get_instance()

        # Query the RAG system
        answer = service.rag_system.query(question)

        # Prepare response
        response: dict[str, Any] = {
            "success": True,
            "answer": answer,
            "sources": [],
        }

        # Get source documents if requested
        if include_sources:
            source_docs = service.rag_system.retrieve_only(question, top_k=top_k)

            # Enrich sources with video URLs
            video_service = get_video_service()
            for doc in source_docs:
                metadata = doc.get("metadata", {})
                video_id = metadata.get("video_id")

                if video_id:
                    # Add video URLs to metadata
                    metadata["video_url"] = video_service.get_video_url(video_id)
                    metadata["video_view_url"] = video_service.get_view_url(video_id)
                    metadata["video_download_url"] = video_service.get_download_url(video_id)
                    metadata["has_video"] = video_service.has_video(video_id)
                else:
                    metadata["has_video"] = False

            response["sources"] = source_docs

        return response

    except Exception as e:
        # Return error response
        return {
            "success": False,
            "answer": "",
            "sources": [],
            "error": str(e),
        }


def retrieve_similar_signs(
    query: str,
    top_k: int = 5,
) -> dict[str, Any]:
    """
    Retrieve similar sign language entries without LLM generation.

    This function is useful for quick lookups or when you just want
    to see similar entries without generating a full answer.

    Args:
        query: Search query (word or description)
        top_k: Number of results to return

    Returns:
        dict with keys:
            - success (bool): Whether the retrieval was successful
            - results (list): List of similar documents
            - error (str): Error message (if success=False)

    Example:
        >>> result = retrieve_similar_signs("xin ch�o", top_k=5)
        >>> for doc in result["results"]:
        >>>     print(doc["metadata"]["word"])
    """
    try:
        # Get singleton instance
        service = RAGServiceSingleton.get_instance()

        # Retrieve similar documents
        results = service.rag_system.retrieve_only(query, top_k=top_k)

        # Enrich results with video URLs
        video_service = get_video_service()
        for doc in results:
            metadata = doc.get("metadata", {})
            video_id = metadata.get("video_id")

            if video_id:
                metadata["video_url"] = video_service.get_video_url(video_id)
                metadata["video_view_url"] = video_service.get_view_url(video_id)
                metadata["video_download_url"] = video_service.get_download_url(video_id)
                metadata["has_video"] = video_service.has_video(video_id)
            else:
                metadata["has_video"] = False

        return {
            "success": True,
            "results": results,
        }

    except Exception as e:
        return {
            "success": False,
            "results": [],
            "error": str(e),
        }


def get_rag_stats() -> dict[str, Any]:
    """
    Get statistics about the RAG system.

    Returns:
        dict with keys:
            - initialized (bool): Whether RAG system is initialized
            - collection_name (str): ChromaDB collection name
            - document_count (int): Number of documents in the database
            - model (str): LLM model being used
            - embedding_model (str): Embedding model being used
    """
    try:
        service = RAGServiceSingleton.get_instance()

        return {
            "initialized": RAGServiceSingleton._initialized,
            "collection_name": service.vector_db.collection_name,
            "document_count": service.vector_db.count(),
            "model": config.openai_model,
            "embedding_model": config.openai_embedding_model,
        }

    except Exception as e:
        return {
            "initialized": False,
            "error": str(e),
        }
