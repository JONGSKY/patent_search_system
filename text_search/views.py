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


from django.core import serializers


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


patent_id_list=None

def text_result(request):
    global patent_id_list
    final_keyword = request.GET['keyword']
    keyword_list = [word.lower().strip() for word in final_keyword.split() if word!='and']
    # 특허는 최신순서로 정렬
    time_1 = datetime.now()
    print(time_1)
    # data_list = Patent.objects.filter(reduce(operator.and_, (Q(abstract__contains=k) for k in keyword_list))).order_by('-date')[:10000]
    # data_list = Patent.objects.filter(reduce(operator.and_, (Q(abstract__contains=k) for k in keyword_list))).order_by('-date')
    data_list = Patent.objects.filter(reduce(operator.and_, (Q(abstract__contains=k) for k in keyword_list)))
    time = datetime.now()
    print(time-time_1)
    print(len(data_list))
    data_list = list(data_list.values('patent_id', 'title', 'abstract', 'country', 'date'))
    time = datetime.now()
    print(time - time_1)
    patent_id_list = [data['patent_id'] for data in data_list]
    time = datetime.now()
    print(time-time_1)
    # result = {"data_list" : data_list,}
    # return JsonResponse(result, safe=False)

    # serialized_qs = serializers.serialize('json', data_list)
    # print(serialized_qs)
    data = {"data_list": data_list}
    return JsonResponse(data)

import json


from sklearn.cluster import KMeans

def clustering_map(request):
    global patent_id_list

    time_1 = datetime.now()
    print(time_1)
    # patent_id_list = request.GET['patent_id'].split(',')

    cluster_patent_id = []
    cluster_embedding = []
    for i in patent_id_list:
        index_ = patent_list.index(int(i))
        cluster_patent_id.append(int(i))
        cluster_embedding.append(embedding_list[index_])

    time = datetime.now()
    print(time-time_1)
    tsne = TSNE(learning_rate=100)
    transformed = tsne.fit_transform(cluster_embedding)
    time = datetime.now()
    print(time-time_1)
    kmeans = KMeans(n_clusters=10, n_jobs=-1)
    kmeans.fit(cluster_embedding)
    time = datetime.now()
    print(time-time_1)
    # print(kmeans.labels_)
    # print(datetime.now())
    # df_new = pd.DataFrame()
    # df_new['x'] = transformed[:, 0]
    # df_new['y'] = transformed[:, 1]
    labels = kmeans.labels_.astype(str).tolist()
    labels = list(map(lambda x: "cluster_"+x, labels))

    b_x = max(transformed[:, 0]).tolist()
    s_x = min(transformed[:, 0]).tolist()
    b_y = max(transformed[:, 1]).tolist()
    s_y = min(transformed[:, 1]).tolist()
    xy_value = [{'x_value': x, "y_value": y, "cluster": label} for label, (x, y) in zip(labels, transformed.tolist())]
    axis_value =  {'b_x':b_x, 's_x':s_x, 'b_y':b_y, 's_y':s_y}
    time = datetime.now()
    print(time-time_1)
    # result = {"x_value" : transformed[:, 0].tolist(),
    #             "y_value" : transformed[:, 1].tolist()}
    # print(type(result['x_value'].tolist()[0]))
    # print(result)
    # result = serialize('json', result)
    # result = json.dumps(result, cls=NumpyEncoder)
    # result = json.dumps(str(result))
    # result = serializers.serialize("json", result)
    # print(result)
    result = {'xy': xy_value, 'axis': axis_value}
    return JsonResponse(result, safe=False)