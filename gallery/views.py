from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from codes.img_to_text import GetTextEmbedding
from .models import Image
from .tasks import *
import numpy as np
import torch
import clip
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from codes.faiss_index import FaissSearchEngine

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

def search_images(request):  # TODO: TEST this function !!
    query = request.GET.get("query", "").strip().lower()
    results = []

    embedder = GetTextEmbedding()

    if query:
        query_embedding = embedder.get_embedding(query)
        engine = FaissSearchEngine()
        matches = engine.search(query_embedding, top_k=5)

        results = Image.objects.filter(id__in=[m["id"] for m in matches])
        # puedes ordenar por distancia si deseas
        results = sorted(results, key=lambda x: [m["distance"] for m in matches if m["id"] == x.id][0])

    return render(request, "gallery/search_results.html", {"results": results, "query": query})

'''def search_images(request):
    query = request.GET.get('q', '').strip().lower()
    results = []

    if query:

        embedder = GetTextEmbedding()
        text_input = clip.tokenize([query], truncate=True).to(embedder.device)
        
        with torch.no_grad():
            query_embedding = embedder.model.encode_text(text_input)
            query_embedding = query_embedding.cpu().numpy()[0].astype('float32')

        for img in Image.objects.all().iterator():
            stored_embedding = img.get_embedding()
            
            if stored_embedding is not None:
                
                stored_embedding = stored_embedding.astype('float32')
                stored_embedding = stored_embedding.reshape(-1)

                similarity = cosine_similarity(query_embedding, stored_embedding)
                similarity = float(similarity)
                
                description_words = set(img.description.lower().split())
                query_words = set(query.split())
                description_match = not query_words.isdisjoint(description_words)
                
                if similarity > 0.3 or description_match:
                    results.append({
                        'image': img,
                        'similarity': similarity,
                        'match_type': 'embedding' if similarity > 0.5 else 'description'
                    })

        # Ordenar por similitud descendente
        results.sort(key=lambda x: x['similarity'], reverse=True)
    
    return render(request, 'gallery/search.html', {
        'results': results[:100],  # Limitar resultados
        'query': query,
        'results_count': len(results)
    })'''

@require_POST
def delete_image(request, image_id):
    try:
        image = Image.objects.get(id=image_id)
        image.image_file.delete(save=False)  # Delete the file from storage
        image.delete()
        messages.success(request, "Image deleted successfully.")
    except Image.DoesNotExist:
        messages.error(request, "Image not found.")
    return HttpResponseRedirect(reverse('image_list'))

@require_POST
def delete_all_images(request):
    Image.objects.all().delete()
    messages.success(request, "All images deleted successfully.")
    return HttpResponseRedirect(reverse('image_list'))