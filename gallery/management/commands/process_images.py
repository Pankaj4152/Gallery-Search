from django.core.management.base import BaseCommand
from codes.img_to_text import GenerateImageDescription, GetTextEmbedding
from gallery.image_storage import ImageStorage

class Command(BaseCommand):
    help = 'Process and store images with descriptions and embeddings'

    def add_arguments(self, parser):
        parser.add_argument('image_path', type=str, help='Path to the image file')

    def handle(self, *args, **kwargs):
        image_path = kwargs['image_path']
        describer = GenerateImageDescription()
        embedder = GetTextEmbedding()
        storage = ImageStorage()

        # Generate description and embedding
        description = describer(image_path)
        if description is None:
            self.stdout.write(self.style.ERROR(f"Failed to generate description for {image_path}"))
            return

        embedding = embedder.get_embedding(image_path)
        storage.save_image(image_path, description, embedding)
        self.stdout.write(self.style.SUCCESS(f"Saved image: {image_path}, Description: {description}"))

        # Optional: Test similarity search
        similar_images = storage.search_similarity(embedding, top_k=3)
        self.stdout.write("Top similar images:")
        for result in similar_images:
            self.stdout.write(f"Path: {result['path']}, Description: {result['description']}, Similarity: {result['similarity']}")