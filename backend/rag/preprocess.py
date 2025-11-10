import json
import re
import pandas as pd

#prepare data
class VietnameseSignLanguageData:
    def __init__(self, json_path: str):
        self.json_path = json_path
        self.data = None
        self.df = None

    def load_data(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.df = pd.DataFrame(self.data['data'])
        print(f"Loaded {len(self.df)} sign language entries")
        return self.df

    def preprocess_text(self, text: str) -> str:
        if not text or pd.isna(text):
          return ""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def create_searchable_text(self, row: pd.Series) -> str:
        parts = [row.get('word', '')] #Use word only 
        return " ".join([str(p) for p in parts if p and not pd.isna(p)])

    def prepare_data(self):
        self.df['searchable_text'] = self.df.apply(self.create_searchable_text, axis=1)
        self.df['searchable_text_normalized'] = self.df['searchable_text'].apply(self.preprocess_text)
        print("Data preprocessing complete")
        return self.df