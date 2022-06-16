import json

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse
import django.http as http
import os
from .config import *
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        if request.FILES:
            myFile = None
            for i in request.FILES:
                myFile = request.FILES[i]
            if myFile:
                dir = BASE_DIR
                destination = open(os.path.join(dir, myFile.name),
                                   'wb+')
                for chunk in myFile.chunks():
                    destination.write(chunk)
                destination.close()
            return HttpResponse('ok')
        else:
            return HttpResponse("none")
    else:
        return HttpResponse("upload error")


@csrf_exempt
def getAllModels(request):
    models = ['多项式回归','线性回归']
    resp = [{"value":item,"label":item} for item in models]
    return JsonResponse(resp,safe=False)


@csrf_exempt
def getAllDatasets(request):
    datasets = ['数据集1','数据集2']
    resp = [{"value": item, "label": item} for item in datasets]
    return JsonResponse(resp,safe=False)


@csrf_exempt
def getResultOfModel(request):
    if request.method=='POST':
        data = json.loads(request.body.decode('utf-8'))
        models = data.get('models')
        dataset = data.get('dataset')
        print("models:",models)
        print("dataset:",dataset)
        if len(models)==1:
            return JsonResponse(
            {
                "dataset":[10,11,14,15],
                "model1":[9,11,13.5,14.5],
            }
        ,safe=False)
        else:
            return JsonResponse(
                {
                    "dataset":[10,11,14,15],
                    "model1":[9,11,13.5,14.5],
                    "model2": [9, 11, 13.5, 14.5],
                }
            ,safe=False)