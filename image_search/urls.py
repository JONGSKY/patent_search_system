from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='image_search'),
    path('2', views.index_2, name='image_search_2'),
    path('image_upload', views.image_upload, name='image_upload'),
]
