from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from gensim.models import KeyedVectors
from text_search.models import Patent
from django.db.models import Q

from functools import reduce
import operator

model = KeyedVectors.load('glove_word2vec_format.model')


def index(request):
    context = {
    }
    return render(request, 'text_search/index.html', context)

def index_2(request):
    return render(request, 'text_search/index_2.html')


def wordcloud_search(request):
    search_keyword = request.GET['keyword']
    list_search_keyword = [word.lower().strip() for word in search_keyword.split()]
    try:
        similar_words = model.wv.most_similar(list_search_keyword, topn=30)
        similar_words = [{'word': w, 'size': 60 - (i * 1.5)} for i, (w, _) in enumerate(similar_words)]
    except Exception:
        similar_words = []
    context = {"myWords": similar_words}
    return JsonResponse(context)


def text_result(request):
    final_keyword = request.GET['keyword']
    keyword_list = final_keyword.split()
    data_list = Patent.objects.filter(reduce(operator.and_, (Q(abstract__contains=k) for k in keyword_list)))
    data_list = data_list[:9]
    data_list = list(data_list.values())
    return JsonResponse(data_list, safe=False)
