from model.model_file import prophetModel, GMModel
from model import myGM as data_preprocess

import os
import pandas as pd

## change this to your laptop directory
BASE_DIR = 'D:\dblab3\prophet-backend\data\datasets'


def getResultOfDataset_prophet(dataset):
    data = pd.read_excel(os.path.join(BASE_DIR, dataset), header=0, skiprows=0).to_numpy().transpose().tolist()
    model = prophetModel()
    model.fit(data[0], data[1])
    predict = model.predict(data[0][0], len(data[0]), 0)
    return predict.to_numpy().tolist()


def getResultWithParams_prophet(dataset,params):
    data = pd.read_excel(os.path.join(BASE_DIR, dataset), header=0, skiprows=0).to_numpy().transpose().tolist()
    model = prophetModel(params["n_changepoints"],params["changepoint_prior_scale"],params["seasonality_prior_scale"],"log")
    model.fit(data[0], data[1])
    predict = model.predict(data[0][0], len(data[0]), params["years"])
    return predict.to_numpy().tolist()


def fit_GM(dataset,params=[1, 0.4, 0]):
    data = pd.read_excel(os.path.join(BASE_DIR, dataset), header=0, skiprows=0)
    model = GMModel(params[0], params[1], params[2])
    data = data_preprocess.preprocess(data)
    origin, fit = model.fit(data)
    return origin.to_numpy().tolist(), fit.to_numpy().tolist()

## dataset:数据集文件名  years: 预测的年份数，比如说数据集最后一年是2020年，需要预测到2024年，则years = 4
def pred_GM(dataset, years, params=[1, 0.4, 0]):
    data = pd.read_excel(os.path.join(BASE_DIR, dataset), header=0, skiprows=0)
    model = GMModel(params[0], params[1], params[2])
    data = data_preprocess.preprocess(data)
    origin,predict = model.pred(data, years)
    return origin.to_numpy().tolist(), predict.to_numpy().tolist()


if __name__=='__main__':
    predict = getResultOfDataset_prophet("三个样本.xlsx")
    print(predict)
