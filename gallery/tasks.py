from codes.img_to_text import GenerateImageDescription
from codes.embedding_extraction import EmbeddingExtractor
from codes.faiss_index import FaissIndexController
from .models import Image
from celery import shared_task
import os

@shared_task(bind=True, max_retries=3)
def process_image_task(self, image_id):
    try:
        image_obj = Image.objects.get(id=image_id)
        img_path = image_obj.image_file.path

        # Generate description, embedding and add it to faiss index
        describer = GenerateImageDescription()
        embedder = EmbeddingExtractor()
        indexer = FaissIndexController()

        description = describer.img_to_text(img_path)
        embedding = embedder.get_embedding(description)
        indexer.add_img_to_idx(image_obj)

        image_obj.description = description
        image_obj.set_embedding(embedding)
        image_obj.save()
        return f"Processed image {image_obj.id} successfully."
    except Exception as e:
        raise self.retry(exc=e, countdown=20)

