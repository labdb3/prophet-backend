import os
from .config import *
import pymongo

"""
Example 1:
    input:三个样本_样本1
    output:[三个样本.xlsx,样本1]
"""
def getFileName(query):
    fileName = None
    for file in os.listdir(BASE_DIR):
        if file.split(".")[0] == query.split("_")[0]:
            fileName = file
            break


    return [fileName,query.split("_")[1]]


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

