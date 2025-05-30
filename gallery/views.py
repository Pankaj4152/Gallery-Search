from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from codes.img_to_text import GenerateImageDescription, GetTextEmbedding
from .image_storage import ImageStorage
from .models import Image
from .tasks import *
import numpy as np
from django.db.models import Q
import torch
import clip
from django.contrib.auth.decorators import login_required

MAX_FILE_SIZE_MB = 5  # Maximum size per image in MB
MAX_TOTAL_STORAGE_MB = 10  # Maximum total storage in MB


def get_total_storage_used(user):
    return sum(img.image_file.size for img in Image.objects.filter(user=user) if img.image_file and img.image_file.size)

@login_required
def upload_image(request):
    # Handle image upload via POST request
    if request.method == 'POST':
        image_files = request.FILES.getlist('image')  # Get list of uploaded files
        if not image_files:
            messages.error(request, "No image files provided.")
            return render(request, 'gallery/upload.html')

        allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']          # Supported MIME types
        success_count = 0                                                               # Track number of successful uploads
        total_storage = get_total_storage_used(request.user)                            # Current storage usage

        for image_file in image_files:
            # Check if the file exceeds the per-file size limit
            if image_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
                messages.warning(request, f"{image_file.name} is too large (>{MAX_FILE_SIZE_MB}MB).")
                continue

            # Check if adding this file would exceed the total storage limit
            if total_storage + image_file.size > MAX_TOTAL_STORAGE_MB * 1024 * 1024:
                messages.error(request, f"Cannot upload {image_file.name}: total gallery storage limit ({MAX_TOTAL_STORAGE_MB}MB) reached.")
                break  # Stop processing further files

            file_type = image_file.content_type
            # Check if the file type is allowed
            if file_type not in allowed_types:
                messages.warning(request, f"Unsupported file type for {image_file.name}. Please upload a JPEG, PNG, JPG, or WEBP image.")
                continue

            # Save the image to the database and filesystem
            image_obj = Image(image_file=image_file, path=image_file.name, user=request.user)
            image_obj.save()
    
            process_image_task.delay(image_obj.id)
            success_count += 1

        if success_count > 0:
            messages.success(request, f'{success_count} image(s) uploaded. Description will be generated shrortly.')
        else:
            messages.error(request, "No valid images were uploaded. Please upload JPEG, PNG, JPG, or WEBP images.")

        return redirect('upload')

    # Render upload page for GET requests
    return render(request, 'gallery/upload.html')

@login_required
def image_list(request):
    # Display all images and storage usage statistics
    images = Image.objects.filter(user=request.user)
    total_storage = get_total_storage_used(request.user)  # in bytes
    max_storage = MAX_TOTAL_STORAGE_MB * 1024 * 1024  # in bytes
    percent_used = int((total_storage / max_storage) * 100) if max_storage else 0
    return render(request, 'gallery/image_list.html', {
        'images': images,
        'total_storage': total_storage,
        'max_storage': max_storage,
        'percent_used': percent_used,
    })

def cosine_similarity(A, B):
    """Compute the cosine similarity between two vectors or matrices."""
    cos = -10    
    dot = np.dot(A, B)
    normb = np.linalg.norm(B)
    
    if len(A.shape) == 1:
        norma = np.linalg.norm(A)
        cos = dot / (norma * normb)
    else: # If A is a matrix, compute the norms of the word vectors of the matrix (norm of each row)
        norma = np.linalg.norm(A, axis=1)
        epsilon = 1.0e-9 
        cos = dot / (norma * normb + epsilon)
        
    return cos

@login_required
def search_images(request):
    # Handle image search by text query
    query = request.GET.get('q', '').strip().lower()
    results = []

    if query:
        # 1. Get normalized embedding for the query using CLIP
        embedder = GetTextEmbedding()
        text_input = clip.tokenize([query], truncate=True).to(embedder.device)
        
        with torch.no_grad():
            query_embedding = embedder.model.encode_text(text_input)
            query_embedding = query_embedding.cpu().numpy()[0].astype('float32')
            query_embedding = query_embedding / np.linalg.norm(query_embedding)

        # 2. Search in images using embedding similarity and description match
        SIMILARITY_THRESHOLD = 0.5  # Set your desired threshold

        for img in Image.objects.filter(user=request.user).iterator():
            stored_embedding = img.get_embedding()
            if stored_embedding is not None:
                # Validate embedding shape and values
                if (
                    stored_embedding.shape != query_embedding.shape
                    or np.isnan(stored_embedding).any()
                ):
                    continue
                norm = np.linalg.norm(stored_embedding)
                if norm == 0:
                    continue
                stored_embedding = stored_embedding / norm

                # Compute cosine similarity between query and image embedding
                similarity = np.dot(query_embedding, stored_embedding)
                # Check if any query word appears in the image description
                description_words = set(img.description.lower().split())
                query_words = set(query.split())
                description_match = not query_words.isdisjoint(description_words)

                # Only append if similarity is above threshold or description matches
                if similarity > SIMILARITY_THRESHOLD or description_match:
                    results.append({
                        'image': img,
                        'similarity': float(similarity),
                        'match_type': 'embedding' if similarity > SIMILARITY_THRESHOLD else 'description'
                    })

        # Sort results by descending similarity
        results.sort(key=lambda x: x['similarity'], reverse=True)
    
    return render(request, 'gallery/search.html', {
        'results': results[:100],  # Limit results
        'query': query,
        'results_count': len(results)
    })

@login_required
@require_POST 
def delete_image(request, image_id):
    # Delete a single image by ID
    try:
        image = Image.objects.get(id=image_id, user=request.user)
        image.image_file.delete(save=False)  # Delete the file from storage
        image.delete()
        messages.success(request, "Image deleted successfully.")
    except Image.DoesNotExist:
        messages.error(request, "Image not found.")
    return HttpResponseRedirect(reverse('image_list'))

@login_required
@require_POST
def delete_all_images(request):
    # Delete all images from the gallery
    Image.objects.filter(user=request.user).delete()
    messages.success(request, "All images deleted successfully.")
    return HttpResponseRedirect(reverse('image_list'))