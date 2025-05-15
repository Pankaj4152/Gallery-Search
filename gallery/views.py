from django.shortcuts import render, redirect
from django.contrib import messages
from codes.img_to_text import GenerateImageDescription, GetTextEmbedding
from .image_storage import ImageStorage
from .models import Image

def upload_image(request):
    if request.method == 'POST':
        image_files = request.FILES.getlist('image')
        if not image_files:
            messages.error(request, "No image files provided.")
            return render(request, 'gallery/upload.html')

        # File type restriction
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
        success_count = 0
        for image_file in image_files:
            file_type = image_file.content_type  # Get the file type from content type
            if file_type not in allowed_types:
                messages.warning(request, f"Unsupported file type for {image_file.name}. Please upload a JPEG, PNG, JPG, or WEBP image.")
                continue

            # Save the image file
            image_obj = Image(image_file=image_file, path=image_file.name)
            image_obj.save()

            # Generate description and embedding
            describer = GenerateImageDescription()
            embedder = GetTextEmbedding()
            image_path = image_obj.image_file.path  # Full path to saved image

            description = describer(image_path)
            if description is None:
                messages.error(request, f"Failed to generate description for {image_file.name}.")
                image_obj.delete()
                continue

            embedding = embedder.get_embedding(image_path)
            image_obj.description = description
            image_obj.set_embedding(embedding)
            image_obj.save()

            success_count += 1

        if success_count:
            messages.success(request, f"{success_count} image(s) uploaded and processed successfully.")
        else:
            messages.error(request, "No images were successfully processed.")

        return redirect('upload')

    return render(request, 'gallery/upload.html')



    #     file_type = imghdr.what(image_file)
    #     if file_type not in allowed_types:
    #         messages.error(request, "Unsupported file type. Please upload a JPEG, PNG, JPG, or WEBP image.")
    #         return render(request, 'gallery/upload.html')

    #     # Save the image file
    #     image_obj = Image(image_file=image_file)
    #     image_obj.save()

    #     # Generate description and embedding
    #     describer = GenerateImageDescription()
    #     embedder = GetTextEmbedding()
    #     image_path = image_obj.image_file.path  # Full path to saved image
    #     image_obj.path = os.path.relpath(image_path, start=os.path.dirname(image_path))  # Store relative path

    #     description = describer(image_path)
    #     if description is None:
    #         messages.error(request, "Failed to generate description.")
    #         image_obj.delete()  # Clean up if processing fails
    #         return render(request, 'gallery/upload.html')

    #     embedding = embedder.get_embedding(image_path)
    #     image_obj.description = description
    #     image_obj.set_embedding(embedding)
    #     image_obj.save()

    #     # Save to ImageStorage (optional, for consistency with existing logic)
    #     storage = ImageStorage()
    #     storage.save_image(image_obj.path, description, embedding)

    #     messages.success(request, f"Image uploaded and processed: {description}")
    #     return redirect('upload')

    # return render(request, 'gallery/upload.html')

def image_list(request):
    images = Image.objects.all()
    return render(request, 'gallery/image_list.html', {'images': images})