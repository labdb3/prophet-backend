import pymongo
from model.pred import getResultWithParams_wensi,getResultWithParams_GM,getResultWithParams_prophet,loadModel_prophet,get_fit_GM
from common.common import *


def saveModelToMongo_prophet(params,dataset):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lab3"]
    mycol = mydb["prophet"]
    doc = {
        "name":params["name"],
        "n_changepoints":params["n_changepoints"],
        "changepoint_prior_scale":params["changepoint_prior_scale"],
        "seasonality_prior_scale":params["seasonality_prior_scale"],
        "k":params["k"],
        "dataset":dataset,
    }
    x = mycol.insert_one(doc)

def saveModelToMongo_wensi(params,dataset):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lab3"]
    mycol = mydb["翁氏模型"]
    doc = {
        "name": params["name"],
        "a":params["a"],
        "b":params["b"],
        "c":params["c"],
        "dataset": dataset,
    }
    x = mycol.insert_one(doc)


def saveModelToMongo_GM(params,dataset):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lab3"]
    mycol = mydb["灰度预测"]
    doc = {
        "name": params["name"],
        "nums": params["nums"],
        "peak_rate":params["peak_rate"],
        "option":params["option"],
        "dataset": dataset,
    }
    x = mycol.insert_one(doc)


def deleteModel_mongodb(model,name):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lab3"]
    if model == "prophet":
        mycol = mydb["prophet"]
    elif model == "翁氏模型":
        mycol = mydb["翁氏模型"]
    elif model == "灰度预测":
        mycol = mydb["灰度预测"]

    print("#####" * 50)
    res = None
    for x in mycol.find():
        if x["name"] == name:
            res = x
    if res==None:
        return

    mycol.delete_one(res)


def loadModel_mutli_sub(name,model,years):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lab3"]
    if model == "prophet":
        mycol = mydb["prophet"]
    elif model == "翁氏模型":
        mycol = mydb["翁氏模型"]
    elif model == "灰度预测":
        mycol = mydb["灰度预测"]

    print("#####"*50)
    res = None
    for x in mycol.find():
        if x["name"] == name:
            res = x


    data = GetData(res["dataset"])
    if years > 0:
        for i in range(years):
            data[0].append(data[0][-1] + 1)

    obj = {}
    res["years"] = years
    print("res:",res)
    if model == "prophet":
        obj["model_prophet"], _,__,___,____ = loadModel_prophet(res["dataset"], res)
        obj["model_prophet_dataset_xAxis"] = data[0]
        obj["model_prophet_dataset_yAxis"] = data[1]
        obj["model_prophet_dataset_name"] = res["dataset"]
    elif model == "翁氏模型":
        obj["model_翁氏模型"], _, __, ___ = getResultWithParams_wensi(res["dataset"], res)
        obj["model_翁氏模型_dataset_xAxis"] = data[0]
        obj["model_翁氏模型_dataset_yAxis"] = data[1]
        obj["model_翁氏模型_dataset_name"] = res["dataset"]
    elif model == "灰度预测":
        obj["model_灰度预测"], _ = getResultWithParams_GM(res["dataset"], res)
        obj["model_灰度预测_dataset_xAxis"] = data[0]
        obj["model_灰度预测_dataset_yAxis"] = data[1]
        obj["model_灰度预测_dataset_name"] = res["dataset"]

    return obj