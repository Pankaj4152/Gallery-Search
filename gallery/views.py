from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from codes.img_to_text import GetTextEmbedding
from codes.embedding_extraction import EmbeddingExtractor
from .models import Image
from .tasks import *
import numpy as np
import torch
import clip
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from codes.faiss_index import FaissSearchEngine, FaissIndexController

@ csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image_files = request.FILES.getlist('image')
        if not image_files:
            messages.error(request, "No image files provided.")
            return render(request, 'gallery/upload.html')

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
    
            process_image_task.delay(image_obj.id)
            success_count += 1

        if success_count > 0:
            messages.success(request, f'{success_count} image(s) uploaded. Description will be generated shrortly.')
        else:
            messages.error(request, "No valid images were uploaded. Please upload JPEG, PNG, JPG, or WEBP images.")

        return redirect('upload')

    return render(request, 'gallery/upload.html')

def image_list(request):
    images = Image.objects.all()
    return render(request, 'gallery/image_list.html', {'images': images})

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

def search_images(request): 
    query = request.GET.get("q", "").strip().lower()
    results = []

    if query:
        if len(query.split()) <= 3:
            query = f'An image of {query}'

        embedder = EmbeddingExtractor()
        
        query_embedding = embedder.get_embedding(query)
        engine = FaissSearchEngine()
        matches = engine.search(query_embedding, k=50, threshold=0.30)

        if matches:
            imgs = Image.objects.filter(id__in=[m["id"] for m in matches])
            results = sorted(imgs, key=lambda x: [m['similarity'] for m in matches if m['id'] == x.id][0])
        else:
            messages.warning(request, "No matches found")

    return render(request, "gallery/search.html", {"results": results, "query": query})

@require_POST
def delete_image(request, image_id):
    try:
        image = Image.objects.get(id=image_id)
        image.image_file.delete(save=False)  # Delete the file from storage
        image.delete()

        delete_from_idx = FaissIndexController()
        delete_from_idx.remove_img_from_idx(image_id)

        messages.success(request, "Image deleted successfully.")
    except Image.DoesNotExist:
        messages.error(request, "Image not found.")
    return HttpResponseRedirect(reverse('image_list'))

@require_POST
def delete_all_images(request):
    Image.objects.all().delete()
    messages.success(request, "All images deleted successfully.")
    return HttpResponseRedirect(reverse('image_list'))