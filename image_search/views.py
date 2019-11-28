from django.shortcuts import render
from django.http import HttpResponse
from patent_search_system import settings
from .src import get_embedding, load_images
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import os

def handle_uploaded_file(f):
    path_to_img = settings.MEDIA_ROOT
    img_path = os.path.join(path_to_img, f.name)
    with open(img_path, 'wb+') as destination:
        destination.write(f.read())
    return img_path

def index(request):
    return render(request, 'image_search/index.html')

def image_upload(request):
    if request.method == 'POST':
        filename = handle_uploaded_file(request.FILES['image'])
        embd = get_embedding.get_embedding(filename)
        image_files = np.load('image_files.npy')
        total_embedding = np.load('embeddings.npy')
        distance_matrix = cosine_similarity(embd, total_embedding)
        result = image_files[np.argsort(distance_matrix).reshape(-1)[-5:]]
        print(result)
    return HttpResponse("success")