from django.conf import settings
from PIL import Image
from codes.img_to_text import GenerateImageDescription, GetTextEmbedding
from .models import Image
from celery import shared_task
import os

@shared_task(bind=True, max_retries=3)
def process_image_task(self, image_id):
    try:
        image_obj = Image.objects.get(id=image_id)
        img_path = os.path.join(settings.MEDIA_ROOT, image_obj.image.name)
        img = Image.open(img_path).convert('RGB')

        # Generate description and embedding
        describer = GenerateImageDescription()
        embedder = GetTextEmbedding()
        image_path = image_obj.image_file.path  # Full path to saved image

        description = describer(image_path)

        embedding = embedder.get_embedding(image_path)
        image_obj.description = description
        image_obj.set_embedding(embedding)
        image_obj.save()
        return f"Processed image {image_obj.id} successfully."
    except Exception as e:
        raise self.retry(exc=e, countdown=20)

