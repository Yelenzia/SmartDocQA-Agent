from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .config import settings


class DocumentVectorStore:
    """Local document retriever based on TF-IDF and cosine similarity."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            analyzer="char",
            ngram_range=(1, 3),
            min_df=1,
            sublinear_tf=True,
        )
        self.matrix = None
        self.chunks: List[Dict] = []
        self.backend = "TF-IDF"

    @staticmethod
    def split_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 80,
    ) -> List[str]:
        if not text:
            return []

        chunks = []
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(text):
                break

            start = max(end - overlap, start + 1)

        return chunks

    def build(self, documents: List[Dict]):
        self.chunks = []

        for doc in documents:
            parts = self.split_text(
                doc["text"],
                settings.chunk_size,
                settings.chunk_overlap,
            )

            for i, text in enumerate(parts, start=1):
                self.chunks.append({
                    "text": text,
                    "source": doc["source"],
                    "location": doc["location"],
                    "chunk": i,
                })

        if not self.chunks:
            raise ValueError("文档中没有可用于建立索引的文本。")

        texts = [item["text"] for item in self.chunks]
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, query: str, top_k: int = None) -> List[Dict]:
        if self.matrix is None or not self.chunks:
            return []

        top_k = min(top_k or settings.top_k, len(self.chunks))

        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix)[0]
        indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in indices:
            item = dict(self.chunks[int(idx)])
            item["score"] = float(scores[int(idx)])
            results.append(item)

        return results
