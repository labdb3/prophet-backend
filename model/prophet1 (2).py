import pandas as pd
import numpy as np
from prophet import Prophet


def log(data):
    data = np.log1p(data)
    return data
def antilog(data):
    data = np.exp(data) - 1
    return data

def standard(data):
    data = (data - data.mean()) / (data.std())
    return data
def anti_standard(data):
    data = data*data.std()+data.mean()
    return data

def normalize(data):
    data = (data-data.min())/(data.max()-data.min())
    return data

def anti_normalize(data):
    data = data*(data.max()-data.min())+data.min()
    return data

def nihe_error(y_true, y_pred):
    nihe_error = 0
    count = 0
    for i in range(len(y_true)):
        if y_pred[i] != 0 and y_true[i] != 0:
            nihe_error += y_pred[i] / y_true[i]
            count += 1
    nihe_error = nihe_error / count
    return nihe_error

class MetaModel():
    def __init__(self, n_changepoints, changepoint_prior_scale, seasonality_prior_scale, data_prepare):
        self.n_changepoints = n_changepoints
        self.changepoint_prior_scale = changepoint_prior_scale
        self.seasonality_prior_scale = seasonality_prior_scale
        self.data_prepare = data_prepare

# prophet(n_changepoints:突变性,changepoint_prior_scale:趋势性,seasonality_prior_scale:周期性，data_prepare:数据预处理方式)
class prophet(MetaModel):
    def __init__(self,n_changepoints,changepoint_prior_scale,seasonality_prior_scale,data_prepare):
        MetaModel.__init__(self,n_changepoints,changepoint_prior_scale,seasonality_prior_scale,data_prepare)
        self.model = Prophet(n_changepoints=self.n_changepoints,changepoint_prior_scale=self.changepoint_prior_scale,seasonality_prior_scale=self.seasonality_prior_scale)

    # fit(year:年份list，storage:储量list)
    def fit(self, year: list, storage: list):
        data = {'ds':year,"y":storage}
        data = pd.DataFrame(data)

        for i in range(0, len(data['ds'])):
            data['ds'][i] = str(data['ds'][i])

        print(data)
        # 转换为标准时间戳
        # data['ds'] = pd.to_datetime(data['ds']).dt.strftime('%Y-%m-%d')
        data['ds'] = pd.to_datetime(data['ds'],format='%Y-%m-%d')
        if self.data_prepare == 1:
            data['y'] = log(data['y'])
        elif self.data_prepare == 2:
            data['y'] = standard(data['y'])
        elif self.data_prepare == 3:
            data['y'] = normalize(data['y'])

        print(data)
        self.model.fit(data)
    # predict(start_year:数据起始年份, data_length:输入数据长度, year_length:预测年份长度)
    def predict(self, start_year: int, data_length: int, year_length: int):
        future = []
        for i in range(data_length + year_length):
            future.append([str(start_year + i)])
        future = pd.DataFrame(future)
        future.columns = ['ds']
        future['ds'] = pd.to_datetime(future['ds'],format='%Y-%m-%d')
        print(future.iloc[-10:])
        forecast = self.model.predict(future.iloc[-10:])
        if self.data_prepare == 1:
            forecast['yhat'] = antilog(forecast['yhat'])
        if self.data_prepare == 2:
            forecast['yhat'] = anti_standard(forecast['yhat'])
        if self.data_prepare == 3:
            forecast['yhat'] = anti_normalize(forecast['yhat'])
        return forecast['yhat']

x = prophet(1000,5000,2000,1)
data = pd.read_excel("/Users/zongdianliu/python/myprophet/data/datasets/三个样本.xlsx", sheet_name='样本1',header=0,skiprows=0)
data.columns=['ds','y']
x.fit(data['ds'].values.tolist(),data['y'].values.tolist())
predict = x.predict(data['ds'].values[0],len(data['ds']),5)
print(nihe_error(data['y'].values.tolist(),predict.values.tolist()))
