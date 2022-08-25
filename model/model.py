import pandas as pd
import numpy as np
from prophet import Prophet
import myGM.util
import myGM.xlsx_reader as xlsx_reader
import myGM.data_preprocess as data_preprocess
from .util import *


class MetaModel:
    def __init__(self):
        pass

    def fit(self):
        pass

    def predict(self):
        pass


# prophet(n_changepoints:突变性,changepoint_prior_scale:趋势性,seasonality_prior_scale:周期性，data_prepare:数据预处理方式)
class prophetModel(MetaModel):
    def __init__(self,n_changepoints=1000,changepoint_prior_scale=5000,seasonality_prior_scale=2000,data_prepare="log"):
        super(MetaModel, self).__init__()
        self.n_changepoints = n_changepoints
        self.changepoint_prior_scale = changepoint_prior_scale
        self.seasonality_prior_scale = seasonality_prior_scale
        self.data_prepare = data_prepare
        self.model = Prophet(n_changepoints=self.n_changepoints,changepoint_prior_scale=self.changepoint_prior_scale,seasonality_prior_scale=self.seasonality_prior_scale)

    # fit(year:年份list，storage:储量list)
    def fit(self, year: list, storage: list):
        data = {'ds':year,"y":storage}
        data = pd.DataFrame(data)

        for i in range(0, len(data['ds'])):
            data['ds'][i] = str(data['ds'][i])
        # 转换为标准时间戳
        data['ds'] = pd.to_datetime(data['ds']).dt.strftime('%Y-%m-%d')

        if self.data_prepare == "log":
            data['y'] = log(data['y'])
        elif self.data_prepare == "standard":
            data['y'] = standard(data['y'])
        elif self.data_prepare == "normalize":
            data['y'] = normalize(data['y'])
        self.model.fit(data)
    # predict(start_year:数据起始年份, data_length:输入数据长度, year_length:预测年份长度)
    def predict(self, start_year: int, data_length: int, year_length: int):
        future = []
        for i in range(data_length + year_length):
            future.append([str(start_year + i)])
        future = pd.DataFrame(future)
        future.columns = ['ds']
        future['ds'] = pd.to_datetime(future['ds'])
        forecast = self.model.predict(future)
        if self.data_prepare == "log":
            forecast['yhat'] = antilog(forecast['yhat'])
        if self.data_prepare == "standard":
            forecast['yhat'] = anti_standard(forecast['yhat'])
        if self.data_prepare == "normalize":
            forecast['yhat'] = anti_normalize(forecast['yhat'])
        return forecast['yhat']


class GMModel(MetaModel):
    def __init__(self, nums=1, peak_rate=0.4, option=0):
        super(MetaModel, self).__init__()
        self.nums = nums
        self.peak_rate = peak_rate
        self.option = option

    def fit(self,data):
        return myGM.util.fit(data)

    def predict(self,data,years):
        return myGM.util.predict(data,years)


if __name__=='__main__':
    x = prophetModel(1000,5000,2000,"log")
    data = pd.read_excel("/home/fcg/lzd/prophet-backend/data/datasets/三个样本.xlsx", sheet_name='样本1',header=0,skiprows=0)
    data.columns=['ds','y']
    print(data)
    x.fit(data['ds'].values.tolist(),data['y'].values.tolist())
    predict = x.predict(data['ds'].values[0],len(data['ds']),5)
    # print(nihe_error(data['y'].values.tolist(),predict.values.tolist()))
