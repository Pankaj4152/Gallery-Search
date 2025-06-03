from sentence_transformers import SentenceTransformer
from gallery.models import Image
import pickle

class EmbeddingExtractor:
    def __init__(self, model='all-MiniLM-L6-v2', device='cpu'):
        self.model = SentenceTransformer(model)
        self.device = device

    def get_embedding(self):
        ''' Extract embeddings for image description'''
        for img in Image.objects.exclude(desctription=None):
            if not img.embedding:
                embedding = self.model.encode(img.description, device=self.device)
                img.embedding = pickle.dumps(embedding)
                img.save()

                return f"Embedding of image {img.id} generated."