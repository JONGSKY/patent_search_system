from django.shortcuts import render
from django.http import JsonResponse
from patent_search_system import settings
from image_search.src import get_embedding
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
from text_search.models import Patent


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
        # filename = handle_uploaded_file(request.FILES['image'])
        # embd = get_embedding.get_embedding(filename)
        # image_files = np.load('image_files.npy')
        # total_embedding = np.load('embeddings.npy').reshape(-1, 256)
        # print(embd.shape, total_embedding.shape)
        # distance_matrix = cosine_similarity(embd, total_embedding)
        # result = image_files[np.argsort(distance_matrix).reshape(-1)[-5:]]
        #
        result = ['US4167245-drawings-page-8.png', 'US4167245-drawings-page-10.png',
         'US4233701-drawings-page-2.png', 'US4256111-drawings-page-4.png',
         'US4256111-drawings-page-3.png']

        patent_list = [filename.split('-')[0][2:] for filename in result]
        print(patent_list)
        patent_info = list(Patent.objects.filter(patent_id__in=patent_list).values('patent_id', 'title', 'abstract'))
        print(len(patent_info))

    return JsonResponse(patent_info, safe=False)
