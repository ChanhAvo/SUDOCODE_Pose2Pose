"""
Script to load Vietnamese Sign Language data into ChromaDB Cloud.

This script:
1. Loads data from VSL_DATA.json
2. Preprocesses the data using VietnameseSignLanguageData
3. Uploads documents to ChromaDB Cloud
"""

import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from langchain_openai import OpenAIEmbeddings

from backend.config import config
from backend.core.chromadb import ChromaVectorDB
from backend.core.preprocessor import VietnameseSignLanguageData


def load_data_to_chroma() -> bool:
    """
    Load Vietnamese Sign Language data into ChromaDB Cloud.

    Returns:
        bool: True if successful, False otherwise
    """
    print("=" * 60)
    print("Loading Vietnamese Sign Language Data to ChromaDB Cloud")
    print("=" * 60)

    # Step 1: Load and preprocess data
    print("\n[1/4] Loading and preprocessing data from JSON...")
    json_path = backend_dir.parent / "data" / "VSL_DATA.json"

    if not json_path.exists():
        print(f"❌ Error: JSON file not found at {json_path}")
        return False

    try:
        data_processor = VietnameseSignLanguageData(str(json_path))
        print(f"✓ Loaded {len(data_processor.documents)} documents")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

    # Step 2: Initialize embeddings
    print("\n[2/4] Initializing OpenAI embeddings...")
    try:
        embeddings = OpenAIEmbeddings(
            model=config.openai_embedding_model
        )
        print(f"✓ Using embedding model: {config.openai_embedding_model}")
    except Exception as e:
        print(f"❌ Error initializing embeddings: {e}")
        return False

    # Step 3: Initialize ChromaDB Cloud
    print("\n[3/4] Connecting to ChromaDB Cloud...")
    try:
        vector_db = ChromaVectorDB(
            api_key=config.chroma_api_key,
            tenant=config.chroma_tenant,
            database=config.chroma_database,
            collection_name=config.chroma_collection_name,
            embedding_function=embeddings,
            distance_metric=config.chroma_distance_metric,
        )
        print(f"✓ Connected to database: {config.chroma_database}")
        print(f"✓ Collection: {config.chroma_collection_name}")
    except Exception as e:
        print(f"❌ Error connecting to ChromaDB: {e}")
        return False

    # Step 4: Upload documents
    print(f"\n[4/4] Uploading {len(data_processor.documents)} documents...")
    print("This may take a few minutes...")

    try:
        # Split into batches to avoid overwhelming the API
        batch_size = 100
        total_docs = len(data_processor.documents)
        successful_batches = 0

        for i in range(0, total_docs, batch_size):
            batch = data_processor.documents[i : i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (total_docs + batch_size - 1) // batch_size

            print(f"  Batch {batch_num}/{total_batches}: Uploading {len(batch)} documents...")

            success = vector_db.add_documents(batch)

            if success:
                successful_batches += 1
                print(f"  ✓ Batch {batch_num} uploaded successfully")
            else:
                print(f"  ❌ Batch {batch_num} failed")

        print(f"\n✓ Upload complete: {successful_batches}/{total_batches} batches successful")

        if successful_batches == total_batches:
            print("\n" + "=" * 60)
            print("✅ SUCCESS: All data loaded to ChromaDB Cloud!")
            print("=" * 60)
            return True
        else:
            print("\n" + "=" * 60)
            print("⚠️  WARNING: Some batches failed to upload")
            print("=" * 60)
            return False

    except Exception as e:
        print(f"\n❌ Error uploading documents: {e}")
        return False


def main():
    """Main entry point."""
    try:
        success = load_data_to_chroma()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Upload interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
