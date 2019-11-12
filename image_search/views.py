from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


# def index(request):
#     return HttpResponse("여기에 개발해주세요 image_search")

def index(request):
   context = {
      'test' : 'test하는중입니다. iamge_search'
   }
   return render(request, 'image_search/index.html', context)