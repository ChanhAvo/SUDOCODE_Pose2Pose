from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import pandas as pd
#faiss and embedding
class VSLKnowledgeBase:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.vectorstore = None
        self.retriever = None

    def build_vectorstore(self, path: str = "models/vsl_chroma_index"):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        documents = [
            Document(
                page_content=row["searchable_text_normalized"],
                metadata={
                    "word": row.get("word", ""),
                    "description": row.get("description", ""),
                    "video_id": row.get("_id", ""),
                    "part_of_speech": row.get("tl", ""),
                    "type": row.get("type", ""),
                    "instruction": row.get("instruction", "")
                }
            )
            for _, row in self.df.iterrows()
        ]
        self.vectorstore = Chroma.from_documents(documents, embeddings, persist_directory=path)
        self.vectorstore.persist()
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        print("Data successfully stored in Chroma")

    def keyword_search(self, query: str, n: int = 2, top_k: int = 3):
        def ngrams(text, n):
            tokens = text.lower().split()
            if len(tokens) < n:
                return [" ".join(tokens)]  # fallback for short words
            return [" ".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

        query_ngrams = set(ngrams(query, n))
        scores = []

        for _, row in self.df.iterrows():
            text = f"{row['word']} {row.get('_word', '')}".lower()
            word_ngrams = set(ngrams(text, n))
            overlap = len(query_ngrams & word_ngrams)
            if overlap > 0:
                scores.append((overlap, row))

        if not scores:
            return []

        scores.sort(reverse=True, key=lambda x: x[0])

        # Group same words together
        grouped = {}
        for overlap, row in scores:
            w = row['word']
            grouped.setdefault(w, []).append((overlap, row))

        # Flatten grouped results up to top_k *groups*
        results = []
        for i, (word, group) in enumerate(grouped.items()):
            results.extend(group)
            if len(results) >= top_k * 3:
                break

        return results[:top_k * 3]


    def load(self, path: str):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = Chroma(persist_directory=path,embedding_function=embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        print("Vectorstore loaded successfully!")
