from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='text_search'),
    path('wordcloud_search', views.wordcloud_search, name='text_search_1'),
    path('text_result', views.text_result, name='text_search_2'),

]
