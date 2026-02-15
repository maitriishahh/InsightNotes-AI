import faiss
import numpy as np
import os
import pickle

INDEX_PATH = "rag/faiss_index.bin"
METADATA_PATH = "rag/metadata.pkl"


class VectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension

        if os.path.exists(INDEX_PATH):
            self.index = faiss.read_index(INDEX_PATH)
            with open(METADATA_PATH, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(dimension)
            self.metadata = []

    def add(self, embedding: list, metadata: dict):
        vector = np.array([embedding]).astype("float32")
        self.index.add(vector)
        self.metadata.append(metadata)

    def search(self, embedding: list, top_k: int = 3):
        vector = np.array([embedding]).astype("float32")
        if self.index.ntotal == 0:
            return [],[]

        distances, indices = self.index.search(vector, top_k)

        results = []

        for idx in indices[0]:
            if idx == -1:
                continue
            if 0 <= idx < len(self.metadata):
                results.append(self.metadata[idx])

        return distances[0], results

    def save(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(METADATA_PATH, "wb") as f:
            pickle.dump(self.metadata, f)
