import json
import re

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse
import django.http as http
import os
from .config import *
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from model.pred import *
import pymongo
 

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


@csrf_exempt
def getResultWithParams(request):
    if request.method=='POST':
        data = json.loads(request.body.decode('utf-8'))
        model = data.get('model')
        dataset = data.get('dataset')
        params = data.get("params")

        print("model:",model)
        print("dataset:",dataset)
        print("params:",params)
        fileName = getFileName(dataset)
        data = pd.read_excel(os.path.join(BASE_DIR, fileName), header=0, skiprows=0).to_numpy().transpose().tolist()

        if params["years"]>0:
            for i in range(params["years"]):
                data[0].append(data[0][-1]+1)

        obj = {
            "dataset_xAxis":data[0],
            "dataset_yAxis":data[1]
        }

        if model=="prophet":
            obj["prophet"] = getResultWithParams_prophet(fileName,params)
            

        print(obj)
        return JsonResponse(
            obj,safe=False
        )


@csrf_exempt
def saveModel(request):
    if request.method=='POST':
        data = json.loads(request.body.decode('utf-8'))
        model = data.get('model')
        dataset = data.get('dataset')
        params = data.get("params")

        print("model:",model)
        print("dataset:",dataset)
        print("params:",params)
        
        saveModelToMongo_prophet(params,dataset)

        return HttpResponse("ok")


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



def saveModelToMongo_prophet(params,dataset):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["prophet"]
    mycol = mydb["prophet"]
    doc = {
        "name":params["name"],
        "n_changepoints":params["n_changepoints"],
        "changepoint_prior_scale":params["changepoint_prior_scale"],
        "seasonality_prior_scale":params["seasonality_prior_scale"],
        "dataset":dataset,
    }
    x = mycol.insert_one(doc)


@csrf_exempt
def getModelList_prophet(request):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["prophet"]
    mycol = mydb["prophet"]
    
    res = []
    for x in mycol.find():
        if x["name"]==None:
            continue
        res.append(x["name"])
    
    resp = [{"value":item,"label":item} for item in res]
    return JsonResponse(resp,safe=False)


@csrf_exempt
def loadModel_prophet(request):

    data = json.loads(request.body.decode('utf-8'))
    model = data.get('name')
    years = data.get("years")
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["prophet"]
    mycol = mydb["prophet"]

    

    res = None
    for x in mycol.find():
        if x["name"]==model:
            res = x
    
    
    fileName = getFileName(res["dataset"])
    data = pd.read_excel(os.path.join(BASE_DIR, fileName), header=0, skiprows=0).to_numpy().transpose().tolist()

    
    if years>0:
        for i in range(years):
            data[0].append(data[0][-1]+1)

    

    obj = {
            "dataset_xAxis":data[0],
            "dataset_yAxis":data[1]
        }

    
    res["years"] = years
    obj["prophet"] = getResultWithParams_prophet(fileName,res)
            

    print(obj)
    return JsonResponse(
            obj,safe=False
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

