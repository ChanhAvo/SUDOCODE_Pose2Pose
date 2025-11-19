"""
RAG (Retrieval-Augmented Generation) Core Module.

This module combines document preprocessing, vector storage, and LLM generation
following clean code principles and SOLID design.
"""

from typing import Any, Optional

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from backend.core.chromadb import ChromaVectorDB
from backend.core.preprocessor import VietnameseSignLanguageData
from backend.prompts.rag_prompt import RAG_PROMPT


class RAGSystem:
    """
    Simple RAG system that combines retrieval and generation.

    This class follows the Single Responsibility Principle by focusing on
    coordinating the RAG workflow without handling low-level details.

    Args:
        vector_db: ChromaDB vector database instance
        llm: Language model for generation
        prompt_template: Optional custom prompt template
    """

    def __init__(
        self,
        vector_db: ChromaVectorDB,
        llm: ChatOpenAI,
        prompt_template: Optional[ChatPromptTemplate] = None,
    ):
        """Initialize RAG system with vector DB and LLM."""
        self._vector_db = vector_db
        self._llm = llm
        self._prompt_template = prompt_template or self._create_default_prompt()
        self._chain: Optional[RunnableSerializable] = None

    def _create_default_prompt(self) -> ChatPromptTemplate:
        """
        Create default RAG prompt template using Vietnamese prompt.

        Returns:
            ChatPromptTemplate for RAG generation
        """
        return ChatPromptTemplate.from_template(RAG_PROMPT)

    def _format_documents(self, documents: list[Document]) -> str:
        """
        Format retrieved documents into a single context string.

        Args:
            documents: List of retrieved documents

        Returns:
            Formatted context string
        """
        if not documents:
            return "Không tìm thấy thông tin liên quan."

        formatted_parts = []
        for i, doc in enumerate(documents, 1):
            metadata = doc.metadata
            formatted_parts.append(
                f"[{i}] Từ: {metadata.get('word', 'N/A')}\n"
                f"Mô tả: {metadata.get('description', 'N/A')}\n"
                f"Từ loại: {metadata.get('part_of_speech', 'N/A')}\n"
                f"Mã video: {metadata.get('video_id', 'N/A')}\n"
                f"Hướng dẫn thực hiện:\n{metadata.get('instruction', 'N/A')}\n"
            )

        return "\n".join(formatted_parts)

    def build_chain(self) -> RunnableSerializable:
        """
        Build the RAG chain combining retrieval and generation.

        Returns:
            Runnable chain for RAG execution
        """
        # Create retrieval chain
        retrieval_chain = {
            "context": self._vector_db.retriever | self._format_documents,
            "question": RunnablePassthrough(),
        }

        # Combine with LLM generation
        self._chain = retrieval_chain | self._prompt_template | self._llm

        return self._chain

    def query(self, question: str) -> str:
        """
        Query the RAG system with a question.

        Args:
            question: User's question

        Returns:
            Generated answer based on retrieved context

        Raises:
            RuntimeError: If chain hasn't been built yet
        """
        if self._chain is None:
            raise RuntimeError("Chain not built. Call build_chain() first.")

        response = self._chain.invoke(question)
        return response.content

    def retrieve_only(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        Retrieve relevant documents without generation.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of retrieved documents with metadata
        """
        # Use the vector DB's retriever
        documents = self._vector_db.retriever.invoke(query)

        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
            for doc in documents[:top_k]
        ]


class RAGBuilder:
    """
    Builder class for constructing RAG systems with proper configuration.

    This class follows the Builder pattern to simplify RAG system construction.
    """

    def __init__(self):
        """Initialize builder with default values."""
        self._vector_db: Optional[ChromaVectorDB] = None
        self._llm: Optional[ChatOpenAI] = None
        self._prompt_template: Optional[ChatPromptTemplate] = None

    def with_vector_db(
        self,
        api_key: str,
        tenant: str,
        database: str,
        collection_name: str,
        embedding_function: OpenAIEmbeddings,
        distance_metric: str = "cosine",
    ) -> "RAGBuilder":
        """
        Configure vector database.

        Args:
            api_key: ChromaDB Cloud API key
            tenant: ChromaDB Cloud tenant ID
            database: ChromaDB Cloud database name
            collection_name: Collection name
            embedding_function: Embedding function
            distance_metric: Distance metric

        Returns:
            Self for method chaining
        """
        self._vector_db = ChromaVectorDB(
            api_key=api_key,
            tenant=tenant,
            database=database,
            collection_name=collection_name,
            embedding_function=embedding_function,
            distance_metric=distance_metric,
        )
        return self

    def with_llm(
        self,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        api_key: Optional[str] = None,
    ) -> "RAGBuilder":
        """
        Configure language model.

        Args:
            model: OpenAI model name
            temperature: Temperature for generation
            api_key: Optional OpenAI API key

        Returns:
            Self for method chaining
        """
        self._llm = ChatOpenAI(
            model=model,
            temperature=temperature
        )
        return self

    def with_custom_prompt(self, prompt_template: ChatPromptTemplate) -> "RAGBuilder":
        """
        Configure custom prompt template.

        Args:
            prompt_template: Custom prompt template

        Returns:
            Self for method chaining
        """
        self._prompt_template = prompt_template
        return self

    def build(self) -> RAGSystem:
        """
        Build and return the RAG system.

        Returns:
            Configured RAG system

        Raises:
            ValueError: If required components are missing
        """
        if self._vector_db is None:
            raise ValueError("Vector database must be configured")
        if self._llm is None:
            raise ValueError("Language model must be configured")

        return RAGSystem(
            vector_db=self._vector_db,
            llm=self._llm,
            prompt_template=self._prompt_template,
        )


class RAGIndexer:
    """
    Helper class for indexing documents into the RAG system.

    This class handles the indexing phase of RAG, separating concerns
    from the query/generation phase.
    """

    @staticmethod
    def index_from_json(
        json_path: str,
        vector_db: ChromaVectorDB,
    ) -> bool:
        """
        Index Vietnamese Sign Language data from JSON file.

        Args:
            json_path: Path to JSON data file
            vector_db: Vector database to store documents

        Returns:
            True if indexing was successful

        Raises:
            FileNotFoundError: If JSON file doesn't exist
            ValueError: If data preprocessing fails
        """
        # Load and preprocess data
        data_processor = VietnameseSignLanguageData(json_path)

        # Add documents to vector database
        success = vector_db.add_documents(data_processor.documents)

        if success:
            print(f"Successfully indexed {len(data_processor.documents)} documents")
        else:
            print("Failed to index documents")

        return success

    @staticmethod
    def index_documents(
        documents: list[Document],
        vector_db: ChromaVectorDB,
    ) -> bool:
        """
        Index a list of documents directly.

        Args:
            documents: List of LangChain documents
            vector_db: Vector database to store documents

        Returns:
            True if indexing was successful
        """
        if not documents:
            print("No documents to index")
            return False

        success = vector_db.add_documents(documents)

        if success:
            print(f"Successfully indexed {len(documents)} documents")
        else:
            print("Failed to index documents")

        return success
