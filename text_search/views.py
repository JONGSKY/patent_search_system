from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from gensim.models.word2vec import Word2Vec
from text_search.models import Patentsview as Patent
from text_search.models import PatentEmbedding
from text_search.models import PatentNgram
from django.db.models import Q
from text_search.utils import *
from django.core import serializers
#
# import re
# import json
import pickle
import operator
import multiprocessing
from functools import reduce
from datetime import datetime

import numpy as np
# from sklearn.manifold import TSNE
from MulticoreTSNE import MulticoreTSNE as TSNE
from sklearn.cluster import KMeans


model = Word2Vec.load('word2vec.model')
# patent_list, embedding_list = pickle.load(open("patent_field_best_model.embed", "rb"))


def index(request):
    return render(request, 'text_search/index.html')


def wordcloud_search(request):
    search_keyword = request.GET['keyword']
    list_search_keyword = [word.lower().strip() for word in search_keyword.split() if word != 'and']
    try:
        similar_words = model.wv.most_similar(list_search_keyword, topn=30)
        similar_words = [{'word': w, 'size': 60 - (i * 1.5)} for i, (w, _) in enumerate(similar_words)]
    except Exception:
        similar_words = []
    context = {"myWords": similar_words}
    return JsonResponse(context)


patent_id_list = []


def text_result(request):
    global patent_id_list
    final_keyword = request.GET['keyword']
    keyword_list = [word.lower().strip() for word in final_keyword.split() if word != 'and']
    # 특허는 최신순서로 정렬
    time_1 = datetime.now()
    print(time_1)
    # data_list = Patent.objects.filter(reduce(operator.and_, (Q(abstract__contains=k) for k in keyword_list))).order_by('-date')[:10000]
    # data_list = Patent.objects.filter(reduce(operator.and_, (Q(abstract__contains=k) for k in keyword_list))).order_by('-date')
    data_list = Patent.objects.filter(reduce(operator.and_, (Q(abstract__contains=k) for k in keyword_list))).order_by('-date')[:100]
    time = datetime.now()
    print(time-time_1)
    time_1 = time

    data_list = list(data_list.values())
    # data_list = data_list.values('patent_id', 'title', 'abstract', 'country', 'date', 'kind', 'number')
    #data_list = data_list.values_list('patent_id', 'title', 'abstract', 'country', 'date', 'kind', 'number')

    patent_id_list = [data['patent_id'] for data in data_list]
    result = {"data_list": data_list}

    time = datetime.now()
    print(time-time_1)

    return JsonResponse(result, safe=False)

    # serialized_qs = serializers.serialize('json', data_list)
    # time = datetime.now()
    # print(time - time_1)
    # return HttpResponse(serialized_qs, content_type='application/json; charset=UTF-8')


def tsne_transform(data, lr=100, n_jobs=-1):
    tsne = TSNE(learning_rate=lr, n_jobs=n_jobs)
    transformed = tsne.fit_transform(data)
    return transformed

    # return transformed[:, 0].tolist(), transformed[:, 1].tolist()


def kmeans_clustering(data, n_cluster=9, n_jobs=-1):
    kmeans = KMeans(n_clusters=n_cluster, n_jobs=n_jobs)
    kmeans.fit(data)
    return kmeans.labels_


# from tsnecuda import TSNE
from collections import defaultdict

#
# def tsne_transform(data):
#     tsne = TSNE()
#     transformed = tsne.fit_transform(data)
#     return transformed
#     # return transformed[:, 0].tolist(), transformed[:, 1].tolist()

#
# def kmeans_clustering(data, n_cluster=10):
#     kmeans = KMeans(n_clusters=n_cluster)
#     kmeans.fit(data)
#     return kmeans.labels_

#
# def convert_string_to_npy(data):
#     data['embedding'] = np.fromstring(data['embedding'], dtype=np.float32, sep=' ')
#     return data['patent_id'], data['embedding']
#
#
# def get_patent_embedding(query_data):
#     with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
#         patent_embedding = list(p.imap(convert_string_to_npy, query_data))
#     return zip(*patent_embedding)
#
#
# def convert_string_to_list(data):
#     return data['embedding'].split(", ")
#
#
# def get_patent_ngram(query_data):
#     with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
#         patent_ngram = list(p.imap(convert_string_to_list, query_data))
#     return patent_ngram
#
#
# from sklearn.feature_extraction.text import TfidfVectorizer
#
#
# tfidf = TfidfVectorizer(
#     analyzer= 'word',
#     tokenizer=lambda x: x,
#     preprocessor=lambda x: x,
#     token_pattern=None,
#     min_df=0.05, max_df=0.95)
#
#
# def get_keywords_using_tfidf(corpus):
#     X = tfidf.fit_transform(corpus)
#     keyword_list = np.array(tfidf.get_feature_names())
#     return keyword_list[np.argsort(np.sum(X.toarray(), axis=0))[-5:]].tolist()


def clustering_map(response):
    global patent_id_list
    global data_list
    time_1 = datetime.now()
    print(time_1)
    # patent_id_list = request.GET['patent_id'].split(',')
    patent_embedding = PatentEmbedding.objects.filter(patent_id__in=patent_id_list).values()

    time = datetime.now()
    print(time-time_1)
    time_1 = time

    patent_ids, embedding_list = get_patent_embedding(patent_embedding)
    embedding_list = np.array(embedding_list)

    time = datetime.now()
    print(time-time_1)
    time_1 = time

    transformed = tsne_transform(embedding_list).tolist()
    # return JsonResponse(transformed, safe=False)

    time = datetime.now()
    print(time-time_1)
    time_1 = time



    labels = kmeans_clustering(embedding_list).tolist()

    time = datetime.now()
    print(time-time_1)
    time_1 = time

    grouped_tsne = defaultdict(list)
    data_list = defaultdict(list)

    for label, pid, xy in zip(labels, patent_ids, transformed):
        grouped_tsne["cluster_"+str(label)].append(xy)
        data_list["cluster_"+str(label)].append(pid)
        # x, y = xy
        # grouped_tsne[label].append({'x': x, 'y': y})


    _grouped_tsne = {}
    _data_list = {}

    for key, patents in data_list.items():
        query_ngram = PatentNgram.objects.filter(patent_id__in=patents).values()
        patent_ngram = get_patent_ngram(query_ngram)
        keywords = get_keywords_using_tfidf(patent_ngram)
        keywords = ",".join(keywords).replace(',','\n')

        _grouped_tsne[keywords] = grouped_tsne[key]
        _data_list[keywords] = data_list[key]

    grouped_tsne = _grouped_tsne
    data_list = _data_list

    del _grouped_tsne
    del _data_list
    #
    #     print(keywords)
    #
    #
    # for label, key, patents in zip(labels, data_list.items()):
    #     query_ngram = PatentTextNgram.objects.filter(patent_id__in=patents).values()
    #     patent_ngram = get_patent_ngram(query_ngram)
    #     keywords = get_keywords_using_tfidf(patent_ngram)
    #     keywords = ", ".join(keywords)
    #     grouped_tsne[keywords] = grouped_tsne.pop(label)
    #     print(keywords)



    # results = []
    # for key in range(10):
    #     print(key, len(grouped_tsne[key]))
    #     results.append({'label': key, 'data': grouped_tsne[key]})
    time = datetime.now()
    print(time-time_1)
    time_1 = time
    if len(patent_id_list)<1000:
        size_data = 10
    elif 1000<=len(patent_id_list)<5000:
        size_data = 8
    else:
        size_data = 5
    results = [{'label': key, 'data': grouped_tsne[key], 'size_data':size_data} for key in grouped_tsne]
    return JsonResponse(results, safe=False)



#     x_values, y_values = tsne_transform(embedding_list)
#
#     time = datetime.now()
#     print(time-time_1)
#
#     labels = kmeans_clustering(embedding_list)
#     labels = list(map(lambda x: "cluster_"+str(x), labels))
#
#
#     time = datetime.now()
#     print(time-time_1)
#
#     # x_values = transformed[:, 0].tolist()
#     # y_values = transformed[:, 1].tolist()
#     #
#     # s_x, b_x = min(x_values), max(x_values)
#     # s_y, b_y = min(y_values), max(y_values)
#     xy_value = [{'x_value': x, "y_value": y, "cluster": label}
#                 for x, y, label in zip(x_values, y_values, labels)]
#
#     axis_value = {'s_x': min(x_values),
#                   'b_x': max(x_values),
#                   's_y': min(y_values),
#                   'b_y': max(y_values)}
#
#     # b_x = max(transformed[:, 0]).tolist()
#     # s_x = min(transformed[:, 0]).tolist()
#     # b_y = max(transformed[:, 1]).tolist()
#     # s_y = min(transformed[:, 1]).tolist()
#
#     time = datetime.now()
#     print(time-time_1)
# # <<<<<<< HEAD
# #     # print(data_list)
# #     return JsonResponse(data_list, safe=False)
# # =======
#     # result = {"x_value" : transformed[:, 0].tolist(),
#     #             "y_value" : transformed[:, 1].tolist()}
#     # print(type(result['x_value'].tolist()[0]))
#     # print(result)
#     # result = serialize('json', result)
#     # result = json.dumps(result, cls=NumpyEncoder)
#     # result = json.dumps(str(result))
#     # result = serializers.serialize("json", result)
#     # print(result)
#     result = {'xy': xy_value, 'axis': axis_value}
#     return JsonResponse(result, safe=False)


def change_data_table(request):
    global data_list
    time_1 = datetime.now()
    print(time_1)
    index = request.GET['index']

    table_list = Patent.objects.filter(patent_id__in=data_list[index]).order_by('-date')

    time = datetime.now()
    print(time-time_1)
    time_1 = time

    table_list = list(table_list.values())

    time = datetime.now()
    print(time-time_1)
    time_1 = time

    result = {"table_list": table_list}

    time = datetime.now()
    print(time-time_1)
    return JsonResponse(result, safe=False)