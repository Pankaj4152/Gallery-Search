import faiss
import numpy as np
from gallery.models import Image
import pickle

class FaissSearchEngine:
    def __init__(self):
        self.index = None
        self.id_map = []

    def build_index(self):
        embeddings = []
        self.id_map = []

        for img in Image.objects.exclude(embedding=None):
            vector = pickle.loads(img.embedding)
            embeddings.append(vector)
            self.id_map.append(img.id)

        if not embeddings:
            return None
        
        embeddings = np.array(embeddings).astype('float32')
        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        
        return self.index
    
    def search(self, query_vec, k=5):
        if self.index is None:
            self.build_index()

        query_vec = np.array(query_vec).astype('float32').reshape(1, -1)
        distances, indices = self.index.search(query_vec, k)

        results = [
            {"id": self.id_map[i], "distance": float(distances[0][rank])}
            for rank, i in enumerate(indices[0])
        ]

        return results
        
    