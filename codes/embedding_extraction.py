from sentence_transformers import SentenceTransformer
from gallery.models import Image
import pickle

class EmbeddingExtractor:
    def __init__(self, model='sentence-transformers/multi-qa-mpnet-base-dot-v1', device='cpu'):
        self.model = SentenceTransformer(model)
        self.device = device

    def get_embedding(self, text):
        ''' Extract embeddings for image description'''
        embedding = self.model.encode(text, normalize_embeddings=True,device=self.device)

        return embedding