from django.shortcuts import render
from django.http import HttpResponse
from patent_search_system import settings

import os


def handle_uploaded_file(f):
    path_to_img = settings.MEDIA_ROOT
    img_path = os.path.join(path_to_img, f.name)
    with open(img_path, 'wb+') as destination:
        destination.write(f.read())


def index(request):
    return render(request, 'image_search/index_2.html')


def image_upload(request):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['image'])
    return HttpResponse("success")
