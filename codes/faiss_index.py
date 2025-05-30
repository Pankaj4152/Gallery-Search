import faiss
import numpy as np
from gallery.models import Image
import pickle
import os

class FaissSearchEngine:
    def __init__(self, index_path='faiss_image.index'):
        self.index = None
        self.index_path  = index_path

    def build_index(self):
        embeddings = []
        ids = []

        for img in Image.objects.exclude(embedding=None):
            vector = pickle.loads(img.embedding)
            embeddings.append(vector)
            ids.append(img.id)

        if not embeddings:
            return None
        
        embeddings = np.array(embeddings).astype('float32')
        dimension = embeddings.shape[1]

        base_index = faiss.IndexFlatL2(dimension)
        self.index = faiss.IndexIDMap(base_index)
        self.index.add_with_ids(embeddings, np.array(ids))
        
        return self.index
    
    def save_index(self):
        if self.index:
            faiss.write_index(self.index, self.index_path)

    def load_index(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            return True
        return False
    
    def refresh_index(self):
        self.build_index()
        self.save_index()

    def search(self, query_vec, k=5):
        if self.index is None:
            if not self.load_index():
                self.build_index()

        if self.index is None:
            return []

        query_vec = np.array(query_vec).astype('float32').reshape(1, -1)
        distances, ids = self.index.search(query_vec, k)

        results = [
            {"id": int(ids[0][rank]), "distance": float(distances[0][rank])}
            for rank in range(len(ids[0]))
            if ids[0][rank] != 1
        ]

        return results
        
    