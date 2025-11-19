"""
ChromaDB Vector Database implementation using Cloud Client.

This module provides a vector database interface following SOLID principles.
Single Responsibility: Handles only vector storage and retrieval operations.
"""

from uuid import uuid4
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document


class ChromaVectorDB:
    """
    ChromaDB Cloud implementation of vector database operations.

    This class follows the Single Responsibility Principle by focusing solely
    on vector database operations without mixing concerns like embedding generation
    or business logic.

    Args:
        api_key: ChromaDB Cloud API key
        tenant: ChromaDB Cloud tenant ID
        database: ChromaDB Cloud database name
        collection_name: Name of the ChromaDB collection
        embedding_function: Optional embedding function (Dependency Inversion)
        distance_metric: Distance metric for similarity search (l2, cosine, ip)
    """

    def __init__(
        self,
        api_key: str,
        tenant: str,
        database: str,
        collection_name: str,
        embedding_function: OpenAIEmbeddings,
        distance_metric: str = "cosine",
    ):
        """Initialize ChromaDB Cloud client and collection."""
        self._api_key = api_key
        self._tenant = tenant
        self._database = database
        self._collection_name = collection_name
        self._distance_metric = distance_metric
        self._embedding_function = embedding_function

        self._collection = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_function,
            chroma_cloud_api_key=api_key,
            tenant=tenant,
            database=database,
        )

    @property
    def retriever(self) -> VectorStoreRetriever:
        """Get the retriever."""
        return self._collection.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 20, "score_threshold": 0.1}
        )

    @property
    def collection_name(self) -> str:
        """Get the collection name."""
        return self._collection_name

    @property
    def database(self) -> str:
        """Get the database name."""
        return self._database

    @property
    def distance_metric(self) -> str:
        """Get the distance metric."""
        return self._distance_metric

    def add_documents(
        self,
        documents: list[Document],
    ) -> bool:
        """
        Add documents to the vector database.

        Args:
            documents: List of document texts to add

        Returns:
            True if documents were added successfully, False otherwise

        Raises:
            ValueError: If documents list is empty or lengths don't match
        """
        if not documents:
            print("Documents list cannot be empty")
            return False

        uuids = [str(uuid4()) for _ in range(len(documents))]

        uuids_added = self._collection.add_documents(documents=documents, ids=uuids)

        if len(uuids_added) != len(documents):
            print(f"Failed to add {len(uuids_added)} documents")
            return False

        return True

    def query_string(self, query: str, top_k: int = 10):
        results = self._collection.similarity_search_with_score(query=query, k=top_k)
        return [
            {
                "document": result[0].page_content,
                "metadata": result[0].metadata,
                "score": result[1],
            }
            for result in results
        ]

    def query_vector(self, query: str, top_k: int = 10):
        results = self._collection.similarity_search_by_vector(
            embedding=self._embedding_function.embed_query(query), k=top_k
        )
        return [
            {
                "document": result.page_content,
                "metadata": result.metadata,
            }
            for result in results
        ]

    def update_documents(
        self,
        documents: list[Document],
    ) -> None:
        """
        Update existing documents in the database.

        Args:
            ids: List of document IDs to update
            documents: New document texts

        Raises:
            ValueError: If ids is empty or lengths don't match
        """
        if not documents:
            raise ValueError("Documents list cannot be empty")
            return

        current_documents_uuids = [str(doc.id) for doc in documents]

        self._collection.update_documents(
            ids=current_documents_uuids, documents=documents
        )

        return

    def delete_documents(self, id: str) -> None:
        """
        Delete documents from the database.

        Args:
            ids: Optional list of document IDs to delete
            where: Optional metadata filter for bulk deletion

        Raises:
            ValueError: If both ids and where are None
        """

        self._collection.delete(id=id)
