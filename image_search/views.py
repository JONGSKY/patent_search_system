from django.shortcuts import render
from django.http import JsonResponse
from patent_search_system import settings
from image_search.src import get_embedding
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os, pickle
from text_search.models import Patent


def handle_uploaded_file(f):
    path_to_img = settings.MEDIA_ROOT
    img_path = os.path.join(path_to_img, f.name)
    with open(img_path, 'wb+') as destination:
        destination.write(f.read())
    return img_path


def index(request):
    return render(request, 'image_search/index.html')

with open('embedding_dictionary.pkl', 'rb') as f:
    embedding_dictionary = pickle.load(f)

image_files = np.asarray(list(embedding_dictionary.keys()))
total_embedding = np.asarray(list(embedding_dictionary.values())).reshape(-1, 256)
del embedding_dictionary

def image_upload(request):
    if request.method == 'POST':
        filename = handle_uploaded_file(request.FILES['image'])
        embd = get_embedding.get_embedding(filename)
        distance_matrix = cosine_similarity(embd, total_embedding)
        result = image_files[np.argsort(distance_matrix).reshape(-1)]
        os.remove(filename)
        patent_list = list()
        image_list = list()
        idx = -1
        while len(patent_list) < 8:
            p_id = result[idx].split('-')[0][2:]
            if p_id not in patent_list:
                patent_list.append(p_id)
                image_list.append(result[idx])
            idx -= 1
        patent_info = list(Patent.objects.filter(patent_id__in=patent_list).values('patent_id', 'title', 'abstract'))
        for value, src in zip(patent_info, image_list):
            value['image_src'] = src
    return JsonResponse(patent_info, safe=False)
