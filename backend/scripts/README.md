# Data Loading Scripts

This directory contains scripts for loading data into ChromaDB Cloud.

## load_data_to_chroma.py

Loads Vietnamese Sign Language data from `data/VSL_DATA.json` into ChromaDB Cloud.

### Prerequisites

1. Create a `.env` file in the project root with the following variables:

```bash
# OpenAI API Key
OPENAI_API_KEY=sk-xxx
OPENAI_EMBEDDING_MODEL=text-embedding-3-large

# ChromaDB Cloud
CHROMA_API_KEY=ck-xxx
CHROMA_TENANT=xxx
CHROMA_DATABASE=pose2pose_vectordb
CHROMA_COLLECTION_NAME=pose2pose_collection
```

2. Ensure the data file exists at `data/VSL_DATA.json`

### Usage

Run from the project root:

```bash
python backend/scripts/load_data_to_chroma.py
```

Or from the backend directory:

```bash
cd backend
python scripts/load_data_to_chroma.py
```

### What it does

1. **Loads data** from `data/VSL_DATA.json`
2. **Preprocesses** using `VietnameseSignLanguageData` class
   - Normalizes text
   - Creates searchable fields
   - Extracts metadata (word, description, video_id, part_of_speech)
3. **Generates embeddings** using OpenAI's embedding model
4. **Uploads to ChromaDB Cloud** in batches of 100 documents
5. **Reports progress** with detailed status messages

### Output

The script provides detailed progress information:

```
============================================================
Loading Vietnamese Sign Language Data to ChromaDB Cloud
============================================================

[1/4] Loading and preprocessing data from JSON...
Loaded 2000 sign language entries
Data preprocessing complete
✓ Loaded 2000 documents

[2/4] Initializing OpenAI embeddings...
✓ Using embedding model: text-embedding-3-large

[3/4] Connecting to ChromaDB Cloud...
✓ Connected to database: pose2pose_vectordb
✓ Collection: pose2pose_collection

[4/4] Uploading 2000 documents...
This may take a few minutes...
  Batch 1/20: Uploading 100 documents...
  ✓ Batch 1 uploaded successfully
  ...

✓ Upload complete: 20/20 batches successful

============================================================
✅ SUCCESS: All data loaded to ChromaDB Cloud!
============================================================
```

### Error Handling

The script includes comprehensive error handling:
- Missing JSON file detection
- Configuration validation
- API connection errors
- Batch upload failures
- Keyboard interrupt handling

### Performance

- Batch size: 100 documents per batch
- Progress reporting for each batch
- Automatic retry on transient failures (handled by ChromaDB client)

### Troubleshooting

**Issue**: `FileNotFoundError: data/VSL_DATA.json not found`
- **Solution**: Ensure the data file exists at the correct path

**Issue**: `ValidationError: CHROMA_API_KEY is required`
- **Solution**: Check your `.env` file has all required ChromaDB settings

**Issue**: API rate limit errors
- **Solution**: The script uses batching to avoid rate limits. If errors persist, reduce batch size in the script.

**Issue**: Some batches fail
- **Solution**: Re-run the script. ChromaDB will skip duplicate documents based on IDs.
