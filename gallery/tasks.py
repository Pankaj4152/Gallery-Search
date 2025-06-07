from codes.img_to_text import GenerateImageDescription
from codes.embedding_extraction import EmbeddingExtractor
from codes.faiss_index import FaissIndexController
from .models import Image
from celery import shared_task, chain

@shared_task(bind=True, max_retries=2)
def generate_description_task(self, image_id):
    try:
        image_obj = Image.objects.get(id=image_id)
        img_path = image_obj.image_file.path

        # Generate description, embedding and add it to faiss index
        describer = GenerateImageDescription()
        description = describer.img_to_text(img_path)

        image_obj.description = description
        image_obj.save()
        return {"image_id": image_obj.id, "description": description}
    except Exception as e:
        raise self.retry(exc=e, countdown=20)

@shared_task(bind=True, max_retries=2)
def  generate_embedding_task(self, data):
    try:
        image_obj = Image.objects.get(id=data['image_id'])
        description = data['description']

        embedder = EmbeddingExtractor()
        indexer = FaissIndexController()
    
        embedding = embedder.get_embedding(description)
        image_obj.set_embedding(embedding)
        image_obj.save()

        indexer.add_img_to_idx(image_obj)
        return f"Processed image {image_obj.id} successfully."
    except Exception as e:
        raise self.retry(exc=e, countdown=20)
        
def process_image_chain(image_id):
    return chain(
        generate_description_task.s(image_id),
        generate_embedding_task.s()
    )

