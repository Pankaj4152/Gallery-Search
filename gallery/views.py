from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from codes.embedding_extraction import EmbeddingExtractor
from .models import Image
from .tasks import *
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from codes.faiss_index import FaissSearchEngine, FaissIndexController
import numpy as np
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
    
            process_image_chain(image_obj.id).delay()
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
        embedder = EmbeddingExtractor()
        
        query_embedding = embedder.get_embedding(query)
        engine = FaissSearchEngine()
        matches = engine.search(query_embedding, k=50, threshold=0.40)

        if matches:
            imgs = Image.objects.filter(id__in=[m["id"] for m in matches])
            results = sorted(imgs, key=lambda x: [m['similarity'] for m in matches if m['id'] == x.id][0])
        else:
            messages.warning(request, "No matches found")

    return render(request, "gallery/search.html", {"results": results, "query": query})

@require_POST
def delete_image(request, image_id):
    # Delete a single image by ID
    try:
        image = Image.objects.get(id=image_id, user=request.user)
        image.image_file.delete(save=False)  # Delete the file from storage
        image.delete()

        delete_from_idx = FaissIndexController()
        delete_from_idx.remove_img_from_idx(image_id)

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