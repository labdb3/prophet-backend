import pandas as pd

import model.myGM.util as util
import numpy as np
from prophet import Prophet
from .util import *
from prophet import Prophet
from scipy.optimize import curve_fit



class MetaModel:
    def __init__(self):
        pass

    def fit(self):
        pass

    def predict(self):
        pass


# prophet(n_changepoints:突变性,changepoint_prior_scale:趋势性,seasonality_prior_scale:周期性，data_prepare:数据预处理方式)
class prophetModel(MetaModel):
    def __init__(self,n_changepoints=1000,changepoint_prior_scale=5000,seasonality_prior_scale=2000,data_prepare="log",k=0):
        super(MetaModel, self).__init__()
        self.n_changepoints = n_changepoints
        self.changepoint_prior_scale = changepoint_prior_scale
        self.seasonality_prior_scale = seasonality_prior_scale
        self.data_prepare = data_prepare
        self.model = Prophet(n_changepoints=self.n_changepoints,changepoint_prior_scale=self.changepoint_prior_scale,seasonality_prior_scale=self.seasonality_prior_scale)
        self.k = k


    # fit(year:年份list，storage:储量list)
    def fit(self, year: list, storage: list):
        data = {'ds':year,"y":storage}
        data = pd.DataFrame(data)

        for i in range(0, len(data['ds'])):
            data['ds'][i] = str(int(data['ds'][i]))
        # 转换为标准时间戳
        data['ds'] = pd.to_datetime(data['ds']).dt.strftime('%Y-%m-%d')

        if self.data_prepare == "log":
            data['y'] = log(data['y'])
        elif self.data_prepare == "standard":
            data['y'] = standard(data['y'])
        elif self.data_prepare == "normalize":
            data['y'] = normalize(data['y'])
        self.model.fit(data)
        if self.k !=0 and self.k !=None:
            self.model.params["k"] = np.array([[self.k]])

        return self.model.params["k"][0][0]
    # predict(start_year:数据起始年份, data_length:输入数据长度, year_length:预测年份长度)
    def predict(self, start_year: int, data_length: int, year_length: int):
        future = []
        for i in range(data_length + year_length):
            future.append([str(int(start_year + i))])
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
    ## nums: 峰点左右点的数目（取两边的最大值，默认为1）
    ## peak_rate: 峰点相比左右临近点最小的增长率（取最大值，默认为0.4）
    ## option: 保留选项，将来用作用户自行划定轮回区间使用
    def __init__(self, nums=1, peak_rate=0.4, option=0, cut_idx = []):
        super(MetaModel, self).__init__()
        self.nums = nums
        self.peak_rate = peak_rate
        self.option = option
        self.cut_idx = cut_idx

    def fit(self, origin_data):
        return util.fit(origin_data, nums=self.nums, peak_rate=self.peak_rate, cut_idx= self.cut_idx)

    def predict(self, origin_data, years):
        return util.predict(origin_data, nums=self.nums, peak_rate=self.peak_rate, years=years, cut_idx= self.cut_idx)


class wenshiModel(MetaModel):
    def __init__(self,a=0,b=0,c=0):
        self.a = a
        self.b = b
        self.c = c

    def fit(self, year: list, storage: list):
        for i in range(len(storage)):
            storage[i] = np.log1p(storage[i])

        year = np.array(year)
        value = np.array(storage)

        def wenshi_function(t, b1, b2, b3):
            return b1 + b2 * np.log(t) + b3 * t
        # 拟合曲线
        print("year:", year)
        print("value:", value)
        parms, _ = curve_fit(wenshi_function, year, value)
        self.a,self.b,self.c = parms

    # predict(a:fit的parms[0], b:fit的parms[1], c:fit的parms[2], year_length:预测年份长度)
    def predict(self,year_length: int):
        x = [i for i in range(1, year_length+1)]
        y = []
        for i in x:
            y.append(np.exp(self.a + self.b * np.log(i) + self.c * i) - 1)
        return y


'''
if __name__=='__main__':
    pass
    # x = wenshiModel()
    # data = pd.read_excel("/Users/zongdianliu/python/prophet-backend/data/datasets/三个样本.xlsx", sheet_name='样本1',header=0,skiprows=0)
    # data.columns=['ds','y']
    # print("data",data)
    # years_data =  [ 7,        10,     12,      24,     26,       30,      35,    36]
    # values_data = [ 112.06,   172.25, 367.96,  467.73, 2098.82,  88.76,   100.0, 100.0]
    # a,b,c=x.fit(years_data,values_data)
    # print("a:",a,"b:",b,"c:",c)
    # predict = x.predict(a,b,c,50)
    # print("predict",predict)
    # print(nihe_error(data['y'].values.tolist(),predict.values.tolist()))

'''

if __name__ == '__main__':
    x = GMModel(nums=1, peak_rate=0.3, option=0)
    data = pd.read_excel("/Users/zongdianliu/python/prophet-backend/data/datasets/三个样本.xlsx", sheet_name="样本1", header=0, skiprows=0)
    predict_data, predict_res = x.predict(data, 5)
    print(data.shape)
    fit_data, fit_res = x.fit(data)
    print(predict_res)



# if __name__=='__main__':
#     x = prophetModel(1000,5000,2000,"log")
#     data = pd.read_excel("/home/fcg/lzd/prophet-backend/data/datasets/三个样本.xlsx", sheet_name='样本1',header=0,skiprows=0)
#     data.columns=['ds','y']
#     print(data)
#     x.fit(data['ds'].values.tolist(),data['y'].values.tolist())
#     predict = x.predict(data['ds'].values[0],len(data['ds']),5)
#     # print(nihe_error(data['y'].values.tolist(),predict.values.tolist()))

