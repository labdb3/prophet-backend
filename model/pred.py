from model.model import prophetModel, GMModel,wenshiModel
from model import myGM as data_preprocess
import os
import pandas as pd
from prophet import Prophet
from .util import *
import pickle

BASE_DIR = '/Users/zongdianliu/python/prophet-backend/data/datasets'


def getFileName(query):
    print('query',query)
    fileName = None
    for file in os.listdir(BASE_DIR):
        if file.split(".")[0] == query.split("_")[0]:
            fileName = file
            break


    return [fileName,query.split("_")[1]]


# 默认参数的模型
def getResultOfDataset_prophet(dataset):
    fileName, sheetName = getFileName(dataset)
    data = pd.read_excel(os.path.join(BASE_DIR, fileName), header=0, skiprows=0,
                         sheet_name=sheetName).to_numpy().transpose().tolist()
    model = prophetModel()
    model.fit(data[0], data[1])
    predict = model.predict(data[0][0], len(data[0]), 0)
    return predict.to_numpy().tolist()


def getResultOfDataset_wensi(dataset):
    fileName, sheetName = getFileName(dataset)
    data = pd.read_excel(os.path.join(BASE_DIR, fileName), header=0, skiprows=0,
                         sheet_name=sheetName).to_numpy().transpose().tolist()
    model = wenshiModel()

    print("data",data)
    # 读取已经标记好的数据集合，如果没有找到，默认使用全部数据集合。
    all_dataset_tag = pickle.load(open(os.path.join(BASE_DIR, 'all_dataset_tag.pkl'), "rb"))
    if dataset in all_dataset_tag.keys():
        print("#####")
        tmp = all_dataset_tag[dataset]
        print(tmp)
        tmp_x = [int(year) - int(data[0][0]) + 1 for year in tmp]
        tmp_y = [data[1][data[0].index(int(year))] for year in tmp]
    else:
        tmp_x = list(range(1, len(data[0]) + 1))
        tmp_y = data[1]

    print("tmpx",tmp_x)
    print("tmpy",tmp_y)
    model.fit(tmp_x,tmp_y)
    pred_y = model.predict(len(data[0]))
    return pred_y

def getResultOfDataset_GM(dataset):
    x = GMModel(nums=1, peak_rate=0.3, option=0)
    fileName, sheetName = getFileName(dataset)
    data = pd.read_excel(os.path.join(BASE_DIR, fileName), sheet_name=sheetName, header=0, skiprows=0)
    predict_data, predict_res = x.predict(data, 5)
    return [item[1] for item in predict_res]


# 自定义参数的模型

def getResultWithParams_prophet(dataset,params):
    fileName, sheetName = getFileName(dataset)
    data = pd.read_excel(os.path.join(BASE_DIR, fileName), header=0, skiprows=0,
                         sheet_name=sheetName).to_numpy().transpose().tolist()

    print("params",params)
    if params["k"]==0 or params["k"]==None:
        model = prophetModel(params["n_changepoints"],params["changepoint_prior_scale"],params["seasonality_prior_scale"],"log")
        k = model.fit(data[0], data[1])
    else:
        model = prophetModel(params["n_changepoints"], params["changepoint_prior_scale"],
                             params["seasonality_prior_scale"], "log",k=params["k"])
        k = model.fit(data[0],data[1])
    predict = model.predict(data[0][0], len(data[0]), params["years"])
    return predict.to_numpy().tolist(),k


def getResultWithParams_wensi(dataset,params):
    fileName, sheetName = getFileName(dataset)
    data = pd.read_excel(os.path.join(BASE_DIR, fileName), header=0, skiprows=0,
                         sheet_name=sheetName).to_numpy().transpose().tolist()
    model = wenshiModel(params["a"],params["b"],params["c"])


    pred_y = model.predict(params["years"]+len(data[0]))
    return pred_y

def getResultWithParams_GM(dataset,params):
    x = GMModel(nums=params["nums"], peak_rate=params["peak_rate"], option=params["option"])
    fileName, sheetName = getFileName(dataset)
    data = pd.read_excel(os.path.join(BASE_DIR, fileName), sheet_name=sheetName, header=0, skiprows=0)
    predict_data, predict_res = x.predict(data, 5)
    return [item[1] for item in predict_res]


if __name__=='__main__':
    predict = getResultOfDataset_prophet("三个样本.xlsx")
    print(predict)
