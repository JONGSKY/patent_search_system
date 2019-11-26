from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from gensim.models.word2vec import Word2Vec
from text_search.models import Patent
from django.db.models import Q

from functools import reduce
import operator

from datetime import datetime

model = Word2Vec.load('word2vec.model')

def index(request):
    return render(request, 'text_search/index.html')


def wordcloud_search(request):
    search_keyword = request.GET['keyword']
    list_search_keyword = [word.lower().strip() for word in search_keyword.split() if word!='and']
    try:
        similar_words = model.wv.most_similar(list_search_keyword, topn=30)
        similar_words = [{'word': w, 'size': 60 - (i * 1.5)} for i, (w, _) in enumerate(similar_words)]
    except Exception:
        similar_words = []
    context = {"myWords": similar_words}
    return JsonResponse(context)

def text_result(request):
    final_keyword = request.GET['keyword']
    keyword_list = [word.lower().strip() for word in final_keyword.split() if word!='and']
    # 특허는 최신순서로 정렬
    time_1 = datetime.now()
    print(time_1)
    data_list = Patent.objects.filter(reduce(operator.and_, (Q(abstract__contains=k) for k in keyword_list))).order_by('-date')
    # data_list = data_list[::-1][:9]
    # data_list = data_list[9::-1]
    time = datetime.now()
    print(time-time_1)
    data_list = data_list[:1000]
    time = datetime.now()
    print(time-time_1)
    data_list = list(data_list.values())
    time = datetime.now()
    print(time-time_1)
    # print(data_list)
    return JsonResponse(data_list, safe=False)
