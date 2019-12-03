from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from gensim.models.word2vec import Word2Vec
from text_search.models import Patent
from django.db.models import Q

from functools import reduce
import operator

from datetime import datetime
# import random
from sklearn.manifold import TSNE
# import pandas as pd
import pickle
import re

model = Word2Vec.load('word2vec.model')
patent_list, embedding_list = pickle.load(open("patent_field_best_model.embed", "rb"))


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

    patent_id_list = list(data_list.values_list('patent_id', flat=True))
    time = datetime.now()
    print(time-time_1)
    # print(len(data_list))
    data_list = data_list[:10000]
    time = datetime.now()
    print(time-time_1)
    data_list = list(data_list.values())
    time = datetime.now()
    print(time-time_1)
    result = {"data_list" : data_list,
                "patent_id_list" : patent_id_list}
    return JsonResponse(result, safe=False)

import json

def clustering_map(request):
    patent_id_list = request.GET['patent_id'].split(',')

    cluster_patent_id = []
    cluster_embedding = []
    for i in patent_id_list:
        number = int(re.findall('\d+', i)[0])
        index_ = patent_list.index(number)
        cluster_patent_id.append(number)
        cluster_embedding.append(embedding_list[index_])

    print(datetime.now())
    tsne = TSNE(learning_rate=100)
    transformed = tsne.fit_transform(cluster_embedding)

    # print(datetime.now())
    # df_new = pd.DataFrame()
    # df_new['x'] = transformed[:, 0]
    # df_new['y'] = transformed[:, 1]
    result = {"x_value" : transformed[:, 0],
                "y_value" : transformed[:, 1]}
    print(result)
    result = json.dumps(str(result))
    return JsonResponse(result, safe=False)