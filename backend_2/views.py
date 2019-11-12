from django.shortcuts import render
from django.http import HttpResponse

# from django.forms.models import model_to_dict
# from backend_1.models import NberCategory
# import json
#
# def index(request):
#    values = NberCategory.objects.all()
#    value_dict = [model_to_dict(val) for val in values]
#    # value_dict = model_to_dict(values)
#    print(value_dict)
#    return HttpResponse(json.dumps(value_dict))


def index(request):
   context = {
      'test' : 'test하는중입니다. backend_2'
   }
   return render(request, 'backend_2/index.html', context)