import json
import re
import pandas as pd  # type: ignore
from langchain_core.documents import Document


# prepare data
class VietnameseSignLanguageData:
    def __init__(self, json_path: str) -> None:
        self.json_path = json_path
        self.data: dict | None = None
        self.df: pd.DataFrame | None = None
        self.documents: list[Document] = []

        self._load_data()
        self._prepare_data()
        self.documents = self._build_documents()

    def _load_data(self) -> pd.DataFrame:
        with open(self.json_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.df = pd.DataFrame(self.data["data"])  # type: ignore
        print(f"Loaded {len(self.df)} sign language entries")

        # Filter to only entries with instruction field
        original_count = len(self.df)
        self.df = self.df[self.df['instruction'].notna() & (self.df['instruction'] != '')]  # type: ignore
        filtered_count = len(self.df)
        print(f"Filtered to {filtered_count} entries with instruction field ({original_count - filtered_count} skipped)")

        return self.df

    def preprocess_text(self, text: str) -> str:  # type: ignore
        if not text or pd.isna(text):
            return ""
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _create_searchable_text(self, row: pd.Series) -> str:  # type: ignore
        parts = [
            row.get("word", ""),
            row.get("instruction", "")  # Include instruction for semantic search
        ]
        return " ".join([str(p) for p in parts if p and not pd.isna(p)])

    def _prepare_data(self) -> pd.DataFrame:
        self.df["searchable_text"] = self.df.apply(self._create_searchable_text, axis=1)  # type: ignore
        self.df["searchable_text_normalized"] = self.df["searchable_text"].apply(  # type: ignore
            self.preprocess_text
        )
        print("Data preprocessing complete")
        return self.df

    def _build_documents(self) -> list[Document]:
        return [
            Document(
                page_content=row["searchable_text_normalized"],
                metadata={
                    "word": row.get("word", ""),
                    "description": row.get("description", ""),
                    "video_id": row.get("_id", ""),
                    "part_of_speech": row.get("tl", ""),
                    "type": row.get("type", ""),
                    "instruction": row.get("instruction", ""),  # Add instruction field
                },
            )
            for _, row in self.df.iterrows()  # type: ignore
        ]
