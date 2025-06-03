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
            try:
                vector = pickle.loads(img.embedding)
                embeddings.append(vector)
                ids.append(img.id)
            except Exception as e:
                print(f"ERROR Failed at loading embedding with id {img.id}: {e}")

        if not embeddings:
            print(f"INFO No embeddings to index")
            return None
        
        embeddings = np.array(embeddings).astype('float32')
        dimension = embeddings.shape[1]

        base_index = faiss.IndexFlatL2(dimension)
        self.index = faiss.IndexIDMap(base_index)
        self.index.add_with_ids(embeddings, np.array(ids, dtype='int64'))
        
        return self.index
    
    def save_index(self):
        if self.index is not None:
            faiss.write_index(self.index, self.index_path)
        else:
            print("WARNING Tried to save an empty index")

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
            print("ERROR Index unable for searching")
            return []

        query_vec = np.array(query_vec).astype('float32').reshape(1, -1)
        distances, ids = self.index.search(query_vec, k)

        results = []
        for rank in range(len(ids[0])):
            image_id = int(ids[0][rank])
            if image_id != -1:  # Faiss usa -1 para resultados no válidos
                results.append({
                    "id": image_id,
                    "distance": float(distances[0][rank])
                })

        return results


class FaissIndexController(FaissSearchEngine):
    def add_img_to_idx(self, img):
        if self.index is None:
            if not self.load_index():
                self.build_index()

        if self.index is None:
            print("ERROR Was not possible to build or load the index")
            return
        
        try:
            v = pickle.loads(img.embedding)
            v = np.array(v).astype('float32').reshape(1, -1)
            self.index.add_with_ids(v, np.array([img.id], dtype='int64'))
            self.save_index()
            return(f"INFO Image ID {img.id} saved to index")
        except Exception as e:
            return(f"ERROR at saving image ID {img.id} to index: {e}")
        
    def remove_img_from_idx(self, img):
        if self.index is None:
            if not self.load_index():
                self.build_index()

        if self.index is None:
            return("ERROR Was not possible to build or load the index")
        
        try:
            self.index.remove_ids(np.array([img.id], dtype='int64'))
            self.save_index()
            return(f"INFO Image ID {img.id} deleted from index")
        except Exception as e:
            return(f"ERROR at removing image ID {img.id} from index: {e}")


        
    