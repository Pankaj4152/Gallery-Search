from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from .models import Image
from .serializers import ImageSerializer
from .tasks import *
from codes.faiss_index import FaissSearchEngine, FaissIndexController
from codes.embedding_extraction import EmbeddingExtractor 

MAX_FILE_SIZE_MB = 5  # Maximum size per image in MB
MAX_TOTAL_STORAGE_MB = 10  # Maximum total storage in MB

def get_total_storage_used(user):
    return sum(img.image_file.size for img in Image.objects.filter(user=user) if img.image_file and img.image_file.size)

class ImageUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        image_files = request.FILES.getlist('image')  
        if not image_files:
            return Response({"error": 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']         
        uploaded_images = []                                                              
        total_storage = get_total_storage_used(request.user)                           

        for f in image_files:
            if f.type not in allowed_types:
                continue
            if f.size > MAX_FILE_SIZE_MB * 1024 * 1024:
                continue
            if total_storage + f.size > MAX_TOTAL_STORAGE_MB * 1024 * 1024:
                break

            image_obj = Image(image_file=f, path=f.name, user=request.user)
            image_obj.save()
            process_image_chain(image_obj.id).delay()
            uploaded_images.append(image_obj)
            total_storage += f.size

        if not uploaded_images:
            return Response({"error": "No images were uploaded due to validation limits."}, status=status.HTTP_400_BAD_REQUEST)
            

        serializer = ImageSerializer(uploaded_images, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED) 

class ImageList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        images = Image.objects.filter(user=request.user)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

class ImageSearch(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.GET.get('q', '').strip().lower()
        if not query:
            return Response({'error': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        embedder = EmbeddingExtractor()
        query_embedding = embedder.get_embedding(query)
        engine = FaissSearchEngine()
        matches = engine.search(query_embedding, k=50, threshold=0.40)

        if not matches:
            return Response([], status=status.HTTP_200_OK)
        
        imgs = Image.objects.filter(id__in=[m["id"] for m in matches])
        results = sorted(imgs, key=lambda x: [m['similarity'] for m in matches if m['id'] == x.id][0])
        serializer = ImageSerializer(results, many=True)
        return Response(serializer.data)

class ImageDelete(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, image_id):
        try:
            image = Image.objects.get(id=image_id, user=request.user)
            image.image_file.delete(save=False)  # Delete the file from storage
            image.delete()

            delete_from_idx = FaissIndexController()
            delete_from_idx.remove_img_from_idx(image_id)

            return Response({'message': 'Image deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Image.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

class DeleteAllImages(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        Image.objects.filter(user=request.user).delete()
        return Response({'message': 'All gallery deleted'}, status=status.HTTP_204_NO_CONTENT)