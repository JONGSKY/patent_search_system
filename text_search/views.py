from django.shortcuts import render
from glove import Corpus, Glove

model = Glove.load('glove_all_200.model')

# Create your views here.
from django.http import HttpResponse

from datetime import datetime

## db에서 patent가져오기
from text_search.models import Patent
from django.db.models import Q

## wordcloud
# from nltk.tokenize import RegexpTokenizer
# from nltk import FreqDist
# from nltk.tag import pos_tag


def index(request):
   context = {
   }
   return render(request, 'text_search/index.html', context)


def wordcloud_search(request):
   search_keyword = request.GET['keyword']

   list_search_keyword = search_keyword.split('and')
   print(list_search_keyword)
   try:
      word_similarity = []
      for keyword in list_search_keyword:
         word_similarity += model.most_similar(keyword.strip().lower(), 30)
      word_similarity = sorted(word_similarity, key=lambda x: x[1], reverse=True)[:30]
   except:
      word_similarity = []
      # similar_words = model.most_similar(search_keyword.lower(), 30)
   print(word_similarity)
   print(len(word_similarity))
   # data_list = Patent.objects.all()[:100]
   # data_list = Patent.objects.filter(abstract__contains=search_keyword)[:2]
   # after = datetime.now()
   # print(after)
   # # retokenize = RegexpTokenizer("[\w]+")
   # names_list = []
   # for data in data_list:
   #    data = data.abstract.lower()
   #    emma_tokens = pos_tag(retokenize.tokenize(data))
   #    noun_list = [t[0] for t in emma_tokens if t[1] == "NN" and t[0] != search_keyword]
   #    names_list += noun_list
   # after_1 = datetime.now()
   # print(after_1)
   # fd_names = FreqDist(names_list)

   context = {
      'search_keyword' : search_keyword,
      # 'myWords': fd_names.most_common(30),
      "myWords" : word_similarity
   }
   return render(request, 'text_search/wordcloud_search.html', context)

def text_result(request):
   final_keyword = request.GET['final_keyword']
   keyword_list = final_keyword.split('and')
   search_keyword = keyword_list[0].strip()

   data_list = Patent.objects.filter(Q(abstract__contains=search_keyword))
   for keyword in keyword_list[1:]:
      data_list = data_list.filter(Q(abstract__contains=keyword))
   data_list = data_list[:9]

   context = {
      'search_keyword': search_keyword,
      'final_keyword' : final_keyword,
      'data_list': data_list,

   }
   return render(request, 'text_search/text_result.html', context)