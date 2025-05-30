import numpy as np
from .models import Image

class ImageStorage:
    def save_image(self, user, image_file, description, embedding):
        ''' Save an image along with its description and embedding.'''
        image = Image(user=user, image_file=image_file, description=description)
        image.set_embedding(embedding)
        image.save()

    # Unused
    def search_similarity(self, query_embedding):
        '''
        Search for images based on multiple criteria:
        1. Word matching with description.
        2. Cosine similarity between query embedding and stored embeddings.
        '''
        score = 0
        for image in Image.objects.all():
            stored_embedding = image.get_embedding()
            similarity = self.cosine_similarity(query_embedding, stored_embedding)

            # Check if the description matches the query
            description_match = any(word in image.description for word in query_embedding)
            if description_match:
                score.append({'path':image.path, 'description':image.description, 'similarity':similarity})
    # Unused
    def cosine_similarity(self, v, w):
        """Compute the cosine similarity between two vectors."""
        return np.dot(v, w) / (np.linalg.norm(v) * np.linalg.norm(w))