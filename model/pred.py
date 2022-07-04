from model.model import prophetModel
import os
import pandas as pd
from prophet import Prophet


BASE_DIR = '/home/fcg/lzd/prophet-backend/data/datasets'


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


if __name__=='__main__':
    predict = getResultOfDataset_prophet("三个样本.xlsx")
    print(predict)
