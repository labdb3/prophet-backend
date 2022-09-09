from model.model import prophetModel, GMModel,wenshiModel
from model import myGM as data_preprocess
import os
import pandas as pd
from prophet import Prophet
import model.myGM.data_preprocess as data_preprocess
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
                         sheet_name=sheetName)
    data = prophet_preprocess(data).to_numpy().transpose().tolist()

    model = prophetModel()
    model.fit(data[0], data[1])
    predict = model.predict(data[0][0], len(data[0]), 0)
    return predict.to_numpy().tolist()


def getResultOfDataset_wensi(dataset):
    fileName, sheetName = getFileName(dataset)
    data = pd.read_excel(os.path.join(BASE_DIR, fileName), header=0, skiprows=0,
                         sheet_name=sheetName).to_numpy().transpose().tolist()
    model = wenshiModel()

    # print("data",data)
    # # 读取已经标记好的数据集合，如果没有找到，默认使用全部数据集合。
    # all_dataset_tag = pickle.load(open(os.path.join(BASE_DIR, 'all_dataset_tag.pkl'), "rb"))
    # if dataset in all_dataset_tag.keys():
    #     print("#####")
    #     tmp = all_dataset_tag[dataset]
    #     print(tmp)
    #     tmp_x = [int(year) - int(data[0][0]) + 1 for year in tmp]
    #     tmp_y = [data[1][data[0].index(int(year))] for year in tmp]
    # else:
    tmp_x = list(range(1, len(data[0]) + 1))
    tmp_y = data[1]


    model.fit(tmp_x,tmp_y)
    pred_y = model.predict(len(data[0]))
    return pred_y

def getResultOfDataset_GM(dataset):
    x = GMModel()
    fileName, sheetName = getFileName(dataset)
    data = pd.read_excel(os.path.join(BASE_DIR, fileName), sheet_name=sheetName, header=0, skiprows=0)
    predict_data, predict_res = x.predict(data, 5)
    return [item[1] for item in predict_res]


# 自定义参数的模型

def getResultWithParams_prophet(dataset,params):
    fileName, sheetName = getFileName(dataset)
    data = pd.read_excel(os.path.join(BASE_DIR, fileName), header=0, skiprows=0,
                         sheet_name=sheetName)
    data = prophet_preprocess(data).to_numpy().transpose().tolist()

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

    if params["a"]==0 and params["b"]==0 and params["c"]==0:
        tmp_x = list(range(1, len(data[0]) + 1))
        tmp_y = data[1]
        model = wenshiModel()
        model.fit(tmp_x, tmp_y)
    else:
        print("当前参数为：",params)
        model = wenshiModel(params["a"],params["b"],params["c"])


    pred_y = model.predict(params["years"]+len(data[0]))
    return pred_y,model.a,model.b,model.c

## origin_data: 文件名
## cur_fit_input: 峰值划定结果
'''
 举例 cur_fit_input = [
[[1966,23.66],[1967, 35.99],[1968,86.22],[1969, 32.33]],
[[1970, 26.67], [1971, 38.89], [1972, 89.27], [1973, 28.35]]
 ]
'''
def getResultWithParams_GM(origin_data, cur_fit_input, params):
    if len(cur_fit_input) <= 1:
        return [], "请至少划分两个旋回，否则无法进行拟合和预测"
    x = GMModel()
    fileName, sheetName = getFileName(origin_data)
    data = pd.read_excel(os.path.join(BASE_DIR, fileName), sheet_name=sheetName, header=0, skiprows=0)
    predict_data, predict_res = x.predict(data, cur_fit_input, 5)
    return [item[1] for item in predict_res]


## 得到数据预处理的结果，方便前端进行数据分段
## 返回值：一个数组，按照年份排列，每个元素是[年份,产量]
def get_preprocess_res(dataset):
    fileName, sheetName = getFileName(dataset)
    data = pd.read_excel(os.path.join(BASE_DIR, fileName), sheet_name=sheetName, header=0,skiprows=0)
    pre = data_preprocess.preprocess(data)
    data = []
    length = len(pre['y'].values)
    for i in range(0, length):
        l = []
        l.append(pre['ds'].values[i])
        l.append(pre['y'].values[i])
        data.append(l)
    return data

if __name__=='__main__':
    predict = getResultOfDataset_prophet("三个样本.xlsx")
    print(predict)
