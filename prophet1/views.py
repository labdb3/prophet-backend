import json

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse
import django.http as http
import os
from .config import *
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from model.pred import *


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
    models = ['prophet']
    resp = [{"value":item,"label":item} for item in models]
    return JsonResponse(resp,safe=False)


@csrf_exempt
def getAllDatasets(request):
    datasets = [file.split(".")[0] for file in os.listdir(BASE_DIR)]
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
        # if len(models)==1:
        #     return JsonResponse(
        #     {
        #         "dataset":[10,11,14,15],
        #         "model1":[9,11,13.5,14.5],
        #     }
        # ,safe=False)
        # else:
        #     return JsonResponse(
        #         {
        #             "dataset":[10,11,14,15],
        #             "model1":[9,11,13.5,14.5],
        #             "model2": [9, 11, 13.5, 14.5],
        #         }
        #     ,safe=False)
        fileName = getFileName(dataset)
        data = pd.read_excel(os.path.join(BASE_DIR, fileName), header=0, skiprows=0).to_numpy().transpose().tolist()

        obj = {
            "dataset_xAxis":data[0],
            "dataset_yAxis":data[1]
        }
        for model in models:
            if model=="prophet":
                obj["prophet"] = getResultOfDataset_prophet(fileName)

        print(obj)
        return JsonResponse(
            obj,safe=False
        )


def getDataset(request):
    query = request.GET.get('dataset', '')
    if query not in [file.split(".")[0] for file in os.listdir(BASE_DIR)]:
        print(query)
        return  HttpResponse("数据集不存在")

    fileName = getFileName(query)

    data = pd.read_excel(os.path.join(BASE_DIR,fileName), header=0, skiprows=0).to_numpy().transpose().tolist()
    print(data)
    return JsonResponse(
        {
            "xAxis":data[0],
            "yAxis":data[1],
        }
    )


"""
Example 1:
    input:三个样本
    output:三个样本.xlsx
"""
def getFileName(query):
    fileName = None
    for file in os.listdir(BASE_DIR):
        if file.split(".")[0] == query:
            fileName = file
            break
    return fileName



if __name__=='__main__':
    data = pd.read_excel("../data/datasets/三个样本.xlsx",header=0, skiprows=0)
    print(data)

