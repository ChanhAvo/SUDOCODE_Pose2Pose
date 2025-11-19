"""
Example usage of the RAG system for Vietnamese Sign Language.

This script demonstrates how to:
1. Set up the RAG system with configuration
2. Index documents from JSON
3. Query the system
"""

from langchain_openai import OpenAIEmbeddings

from backend.config import config
from backend.core import RAGBuilder, RAGIndexer


def main():
    """Main example function."""
    # Step 1: Create embedding function
    embeddings = OpenAIEmbeddings(
        model=config.openai_embedding_model,
        api_key=config.openai_api_key,
    )

    # Step 2: Build RAG system using the builder pattern
    rag_system = (
        RAGBuilder()
        .with_vector_db(
            api_key=config.chroma_api_key,
            tenant=config.chroma_tenant,
            database=config.chroma_database,
            collection_name=config.chroma_collection_name,
            embedding_function=embeddings,
            distance_metric=config.chroma_distance_metric,
        )
        .with_llm(
            model=config.openai_model,
            temperature=0.7,
            api_key=config.openai_api_key,
        )
        .build()
    )

    # Step 3: Index documents (only need to do this once)
    print("Indexing documents from JSON...")
    json_path = "data/sign_language_data.json"  # Update with actual path
    success = RAGIndexer.index_from_json(json_path, rag_system._vector_db)

    if not success:
        print("Failed to index documents. Exiting...")
        return

    # Step 4: Build the RAG chain
    print("\nBuilding RAG chain...")
    rag_system.build_chain()

    # Step 5: Query the system
    print("\nQuerying the RAG system...")
    questions = [
        "Từ 'xin chào' có nghĩa là gì?",
        "Làm thế nào để biểu đạt 'cảm ơn' trong ngôn ngữ ký hiệu?",
        "Tìm thông tin về từ 'yêu'",
    ]

    for question in questions:
        print(f"\n{'='*60}")
        print(f"Câu hỏi: {question}")
        print(f"{'='*60}")

        # Get answer
        answer = rag_system.query(question)
        print(f"Trả lời: {answer}")

    # Step 6: Retrieve only (without generation)
    print(f"\n{'='*60}")
    print("Testing retrieval-only mode...")
    print(f"{'='*60}")

    query = "xin chào"
    results = rag_system.retrieve_only(query, top_k=3)

    print(f"\nTop 3 results for '{query}':")
    for i, result in enumerate(results, 1):
        print(f"\n[{i}]")
        print(f"Content: {result['content']}")
        print(f"Word: {result['metadata'].get('word', 'N/A')}")
        print(f"Description: {result['metadata'].get('description', 'N/A')}")


if __name__ == "__main__":
    main()
