from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from codes.img_to_text import GenerateImageDescription, GetTextEmbedding
from .image_storage import ImageStorage
from .models import Image
from .tasks import process_image_task
import numpy as np
from django.db.models import Q
import torch
import clip

@ csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image_files = request.FILES.getlist('image')
        if not image_files:
            messages.error(request, "No image files provided.")
            return render(request, 'gallery/upload.html')

        # File type restriction
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
        success_count = 0
        img_ids = []
        for image_file in image_files:
            file_type = image_file.content_type  # Get the file type from content type
            if file_type not in allowed_types:
                messages.warning(request, f"Unsupported file type for {image_file.name}. Please upload a JPEG, PNG, JPG, or WEBP image.")
                continue

            # Save the image file
            image_obj = Image(image_file=image_file, path=image_file.name)
            img_ids.append(image_obj.id)
            process_image_task.delay(image_obj.id)
            image_obj.save()

            '''
            if description is None:
                messages.error(request, f"Failed to generate description for {image_file.name}.")
                image_obj.delete()
                continue
            '''
            success_count += 1

        return JsonResponse({
            'message': f"{len(image_files)} received. Processing on background.",
            'img_ids': img_ids,
        })

        '''if success_count:
            messages.success(request, f"{success_count} image(s) uploaded and processed successfully.")
        else:
            messages.error(request, "No images were successfully processed.")'''

        '''return redirect('upload')'''

    return render(request, 'gallery/upload.html')

def image_list(request):
    images = Image.objects.all()
    return render(request, 'gallery/image_list.html', {'images': images})

def cosine_similarity(w, v):
            """Compute the cosine similarity between two vectors."""
            w /= np.linalg.norm(w)
            v /= np.linalg.norm(v)
            return np.dot(w, v)

'''def search_images(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        embedder = GetTextEmbedding()
        text = clip.tokenize([query]).to(embedder.device)
        with torch.no_grad():
            query_embedding = embedder.model.encode_text(text).cpu().numpy()[0]
            query_embedding = query_embedding / np.linalg.norm(query_embedding)  # embedding norm

        for img in Image.objects.all().iterator():
            stored_embedding = img.get_embedding()

            if stored_embedding is not None:
                norm_s_embedding = stored_embedding / np.linalg.norm(stored_embedding)
                similarity = cosine_similarity(query_embedding, norm_s_embedding)

                # Check description matches query
                description_words = img.description.lower().split()
                query_words = query.split()
                description_match = any(word in description_words for word in query_words)

            if similarity > 0.3 or description_match:
                results.append({'image': img, 'similarity': similarity, 'match': 'embedding' if similarity > 0.3 else 'description'})

        results.sort(key=lambda x: (x['similarity'], x.get('match_type') == 'description'),reverse=True)
    return render(request, 'gallery/search.html', {'results': results, 'query': query, 'results_count': len(results)})'''

def search_images(request):
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
    })

from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse

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