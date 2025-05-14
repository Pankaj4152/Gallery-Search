import numpy as np
from .models import Image

class ImageStorage:
    def save_image(self, path, description, embedding):
        """
        Save an image with its path, description, and embedding to the database.
        """
        image = Image(path=path, description=description)
        image.set_embedding(embedding)
        image.save()

    def search_similarity(self, query_embedding, top_k=3):
        """Search for top_k images with highest cosine similarity to query_embedding."""
        results = []
        for image in Image.objects.all():
            # Get the stored embedding
            stored_embedding = image.get_embedding()
            # Calculate cosine similarity
            similarity = self.cosine_similarity(query_embedding, stored_embedding)
            results.append({
                'path': image.path,
                'description': image.description,
                'similarity': similarity
            })

            return sorted(results, key=lambda x: x['similarity'], reverse=True)[:top_k]
        
    def cosine_similarity(self, v, w):
        """Compute the cosine similarity between two vectors."""
        return np.dot(v, w) / (np.linalg.norm(v) * np.linalg.norm(w))