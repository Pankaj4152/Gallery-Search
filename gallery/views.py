from django.shortcuts import render, redirect
from django.contrib import messages
from codes.img_to_text import GenerateImageDescription, GetTextEmbedding
from .image_storage import ImageStorage
from .models import Image
import os

def upload_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        if not image_file:
            messages.error(request, "No image file provided.")
            return render(request, 'gallery/upload.html')

        # Save the image file
        image_obj = Image(image_file=image_file)
        image_obj.save()

        # Generate description and embedding
        describer = GenerateImageDescription()
        embedder = GetTextEmbedding()
        image_path = image_obj.image_file.path  # Full path to saved image
        image_obj.path = os.path.relpath(image_path, start=os.path.dirname(image_path))  # Store relative path

        description = describer(image_path)
        if description is None:
            messages.error(request, "Failed to generate description.")
            image_obj.delete()  # Clean up if processing fails
            return render(request, 'gallery/upload.html')

        embedding = embedder.get_embedding(image_path)
        image_obj.description = description
        image_obj.set_embedding(embedding)
        image_obj.save()

        # Save to ImageStorage (optional, for consistency with existing logic)
        storage = ImageStorage()
        storage.save_image(image_obj.path, description, embedding)

        messages.success(request, f"Image uploaded and processed: {description}")
        return redirect('upload')

    return render(request, 'gallery/upload.html')

def image_list(request):
    images = Image.objects.all()
    return render(request, 'gallery/image_list.html', {'images': images})