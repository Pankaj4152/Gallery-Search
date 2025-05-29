import numpy as np
import faiss

d = 512
index = faiss.IndexFlatL2(d) 

embeddings = np.random.random((512, d)).astype('float32')
index.add(embeddings) 

query = np.random.random((1, d)).astype('float32')
D, I = index.search(query, k=5)

print(f'Nearest neighbors (indices): {I}')
print(f'Distances: {D}')


from django.shortcuts import render
from .faiss_index import FaissSearchEngine
from .img_to_text import GetTextEmbedding
from gallery.models import Image

def search_images(request):
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
