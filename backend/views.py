import json
import pickle
import re

import numpy as np
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .util import *
from data.smoothprocessing import Method1
from common.common import *
import matplotlib.pyplot as plt
import PIL.Image as Image
from io import BytesIO
import base64
import matplotlib
import pymongo
from model.k_means_platform import k_means
matplotlib.use('Agg')
from model.pred import get_sum_fitting

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        if request.FILES:
            myFile = None
            for i in request.FILES:
                myFile = request.FILES[i]
            if myFile:
                dir = DATABASE_PATH
                destination = open(os.path.join(dir, myFile.name),
                                   'wb+')
                for chunk in myFile.chunks():
                    destination.write(chunk)
                destination.close()

                # 读取数据
                all_data = LoadDataBase()
                if myFile.name in all_data.keys():
                    os.remove(os.path.join(dir, myFile.name))
                    return JsonResponse('文件已存在',safe=False)
                all_data[myFile.name]={}
                sheets = pd.read_excel(os.path.join(dir, myFile.name), sheet_name=None)
                # print(sheets)
                for sheet in sheets:
                    data = pd.read_excel(os.path.join(dir, myFile.name), sheet_name=sheet).to_numpy().transpose().tolist()
                    all_data[myFile.name][sheet]={
                        "xAxis":data[0],
                        "yAxis":data[1],
                    }
                DumpDataBase(all_data)

                os.remove(os.path.join(dir, myFile.name))
            return HttpResponse('ok')
        else:
            return HttpResponse("none")
    else:
        return HttpResponse("upload error")

@csrf_exempt
def deleteDataSet(request):
    dataset = request.GET.get('dataset', '')
    fileName,sheetName = getFileName(dataset)
    all_data = LoadDataBase()
    if sheetName in all_data[fileName].keys():
        del all_data[fileName][sheetName]
    if len(all_data[fileName].keys())==0:
        del all_data[fileName]
    DumpDataBase(all_data)
    return JsonResponse({},safe=False)



@csrf_exempt
def getAllMetaModels(request):
    models = ['prophet',"翁氏模型","灰度预测"]
    resp = [{"value":item,"label":item} for item in models]
    return JsonResponse(resp,safe=False)


@csrf_exempt
def getAllDatasets(request):
    all_datasets = []
    all_data = LoadDataBase()
    for fileName in all_data:
        for sheet in all_data[fileName].keys():
            all_datasets.append(fileName+"_"+sheet)


    resp = [{"value": item, "label": item} for item in all_datasets]
    return JsonResponse(resp,safe=False)

@csrf_exempt
def getAllPreprocessMethods(request):
    resp = [
        {"value":"平滑处理","label":"平滑处理"},
    ]
    return JsonResponse(resp,safe=False)


@csrf_exempt
def getResultOfPreprocess(request):
    dataset = request.GET.get('dataset', '')
    method = request.GET.get('method', '')
    window_size = [int(item) for item in list(request.GET.get('window_size','').split(","))]
    print("dataset:",dataset,"method:",method,"window_size",window_size)


    data = GetData(dataset)
    obj = {
        "dataset_xAxis": data[0],
        "dataset_yAxis": data[1],
    }

    for size in window_size:
        _data = Method1(dataset,size)
        obj[method+str(size)]=_data[1]
    return JsonResponse(obj,safe=False)


@csrf_exempt
def saveDataset(request):
    input = json.loads(request.body.decode('utf-8'))
    name = input.get('name')
    data = input.get('data')
    base_data = input.get("base_data")
    window_size = input.get("window_size")
    print("name:",name)
    print("data:",data)
    print("base_data:",base_data)
    print("window_size",window_size)

    if len(data.keys())==0 or len(base_data.keys())==0:
        print("数据为空，保存失败")
        return JsonResponse(name, safe=False)

    # 首先判断是否存在当前sheet
    all_data = LoadDataBase()
    fileName,sheetName = getFileName(name)
    if all_data[fileName] and sheetName in all_data[fileName].keys():
        return JsonResponse(name, safe=False)
    all_data[fileName][sheetName] = {
        "xAxis":base_data["xAxis"],
        "yAxis":data["".join(sheetName.split("_")[-2:])],
    }
    DumpDataBase(all_data)

    return JsonResponse(name,safe=False)


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
        data = GetData(dataset)
        if params["years"]>0:
            for i in range(params["years"]):
                data[0].append(data[0][-1]+1)

        obj = {
            "dataset_xAxis":data[0],
            "dataset_yAxis":data[1]
        }

        def get_loss(a,b):
            sum = 0
            for i in range(len(a)):
                sum +=(a[i]-b[i])*(a[i]-b[i])
            return sum/len(a)

        if model=="prophet":
            obj["prophet"],obj["k"],n_changepoints,changepoint_prior_scale,seasonality_prior_scale = getResultWithParams_prophet(dataset,params)
            print(obj["k"],type(obj["k"]))
            obj["k"] = float(obj["k"])
            obj["loss"] = get_loss(obj["dataset_yAxis"],obj["prophet"])
            obj["n_changepoints"] = n_changepoints
            obj["changepoint_prior_scale"] = changepoint_prior_scale
            obj["seasonality_prior_scale"] = seasonality_prior_scale

        elif model=="翁氏模型":
            obj["翁氏模型"],obj["a"],obj["b"],obj["c"] = getResultWithParams_wensi(dataset,params)
            obj["loss"] = get_loss(obj["dataset_yAxis"], obj["翁氏模型"])
        elif model=="灰度预测":
            obj["灰度预测"],msg = get_predicting_results_with_params_gm(dataset, params)
            _, obj["fit"], obj["Nm_l"], obj["tm_l"], obj["b_l"], obj["color"], _ = get_fit_GM(dataset,params)
            if msg != None:
                obj["msg"] = msg
            else:
                obj["loss"] = get_loss(obj["dataset_yAxis"], obj["灰度预测"])

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

        if model=="prophet":
            saveModelToMongo_prophet(params,dataset)
        elif model=="翁氏模型":
            saveModelToMongo_wensi(params,dataset)
        elif model=="灰度预测":
            saveModelToMongo_GM(params,dataset)
        return HttpResponse("ok")



def getDataset(request):
    query = request.GET.get('dataset', '')
    data = GetData(query)
    cumulative = [data[1][0]]
    for i in range(1,len(data[1])):
        cumulative.append(data[1][i]+cumulative[-1])
    return JsonResponse(
        {
            "name":query,
            "xAxis":data[0],
            "yAxis":data[1],
            "cumulative":cumulative,
        }
    )


@csrf_exempt
def getURL(request):
    return JsonResponse(
        {
            "url":URL,
        }
    )

@csrf_exempt
def getModelList(request):
    model = request.GET.get("model",'')
    dataset = request.GET.get("dataset",'')
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lab3"]
    print(model,dataset)
    if model=="prophet":
        mycol = mydb["prophet"]
    elif model=="翁氏模型":
        mycol = mydb["翁氏模型"]
    elif model=="灰度预测":
        mycol = mydb["灰度预测"]

    res = []
    if dataset=="":
        for x in mycol.find():
            res.append(x["name"])
    else:
        for x in mycol.find():
            if x["dataset"]!= dataset:
                continue
            res.append(x["name"])
    
    resp = [{"value":item,"label":item} for item in res]
    return JsonResponse(resp,safe=False)


@csrf_exempt
def loadModel_multi(request):
    data = json.loads(request.body.decode('utf-8'))
    model = data.get("models")
    years = data.get("years")
    print("models:",model)
    print("years:",years)

    obj = {}
    if model["prophet"][0]!="":
        res = loadModel_mutli_sub(model["prophet"][0],"prophet",years)
        obj.update(res)
    if model["灰度预测"][0] != "":
        res = loadModel_mutli_sub(model["灰度预测"][0], "灰度预测", years)
        obj.update(res)
    if model["翁氏模型"][0] != "":
        res = loadModel_mutli_sub(model["翁氏模型"][0], "翁氏模型", years)
        obj.update(res)

    return JsonResponse(obj,safe=False)


@csrf_exempt
def deleteModel(request):
    model_type = request.GET.get("model_type", '')
    model_name = request.GET.get("model_name",'')
    print("model_type",model_type,"model_name",model_name)
    deleteModel_mongodb(model_type,model_name)
    return JsonResponse({},safe=False)


@csrf_exempt
def loadModel(request):
    data = json.loads(request.body.decode('utf-8'))
    model = data.get("model")
    name = data.get('name')
    years = data.get("years")
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lab3"]
    if model == "prophet":
        mycol = mydb["prophet"]
    elif model == "翁氏模型":
        mycol = mydb["翁氏模型"]
    elif model == "灰度预测":
        mycol = mydb["灰度预测"]

    res = None
    for x in mycol.find():
        if x["name"]==name:
            res = x
    
    
    data = GetData(res["dataset"])
    if years>0:
        for i in range(years):
            data[0].append(data[0][-1]+1)

    obj = {
            "dataset_xAxis":data[0],
            "dataset_yAxis":data[1]
        }

    res["years"] = years

    if model=="prophet":
        obj["prophet"],obj["k"],_,__,___ = loadModel_prophet(res["dataset"],res)
        obj["k"] = float(obj["k"])
    elif model=="翁氏模型":
        obj["翁氏模型"],obj["a"],obj["b"],obj["c"] = getResultWithParams_wensi(res["dataset"],res)
    elif model=="灰度预测":
        obj["灰度预测"],msg = get_predicting_results_with_params_gm(res["dataset"], res)
        if msg!=None:
            obj["msg"] = msg

    print(obj)


    return JsonResponse(
            obj,safe=False
    )



@csrf_exempt
def showPhoto(request):
    x =[1,2,3,4]
    y = [2,3,4,5]
    plt.plot(x,y)
    plt.savefig("demo.jpeg")
    img_file = Image.open("demo.jpeg")
    # 将图片保存到内存中
    f = BytesIO()
    img_file.save(f, 'jpeg')
    # 从内存中取出bytes类型的图片
    data = f.getvalue()
    # 将bytes转成base64
    data = base64.b64encode(data).decode()

    return JsonResponse(data,safe=False)

@csrf_exempt
def showClustering(request):
    data = json.loads(request.body.decode('utf-8'))
    dataname = data.get("name")
    print("--------")
    print(dataname)
    all_data = LoadDataBase()
    sheetname = []
    data = []
    for fileName in all_data.keys():
        for sheetName in all_data[fileName]:
            cur = fileName+"_"+sheetName
            if cur in dataname:
                sheetname.append(fileName+"_"+sheetName)
                data.append(all_data[fileName][sheetName]["yAxis"])



    k_means(sheetname,data)

    return HttpResponse(None)


@csrf_exempt
def getSumFitting(request):
    dataset = request.GET.get("dataset", '')
    sum_file_name, actual_file_name,list = get_sum_fitting(dataset,None)

    img_file = Image.open("static/demo_actual.jpeg")
    # 将图片保存到内存中
    f = BytesIO()
    img_file.save(f, 'jpeg')
    # 从内存中取出bytes类型的图片
    data1 = f.getvalue()
    # 将bytes转成base64
    data1 = base64.b64encode(data1).decode()

    img_file = Image.open("static/demo_sum.jpeg")
    # 将图片保存到内存中
    f = BytesIO()
    img_file.save(f, 'jpeg')
    # 从内存中取出bytes类型的图片
    data2 = f.getvalue()
    # 将bytes转成base64
    data2 = base64.b64encode(data2).decode()

    return JsonResponse({
        "sum":data2,
        "actual":data1,
        "list":list,
    }, safe=False)

