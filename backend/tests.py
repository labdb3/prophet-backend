import pandas as pd
import numpy as np
# from prophet import Prophet
from scipy.optimize import curve_fit


class MetaModel:
    def __init__(self):
        pass

    def fit(self):
        pass

    def predict(self):
        pass

class wenshiModel(MetaModel):
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
        return parms

    # predict(a:fit的parms[0], b:fit的parms[1], c:fit的parms[2], year_length:预测年份长度)
    def predict(self, a: float, b: float, c: float, year_length: int):
        x = [i for i in range(1, year_length)]
        y = []
        for i in x:
            y.append(np.exp(a + b * np.log(i) + c * i) - 1)
        return y


if __name__=='__main__':
    x = wenshiModel()
    data = pd.read_excel("/Users/zongdianliu/python/prophet-backend/data/datasets/三个样本.xlsx", sheet_name='样本1',header=0,skiprows=0)
    data.columns=['ds','y']
    print("data",data)
    years_data =  [ 7,        10,     12,      24,     26,       30,      35,    36]
    values_data = [ 112.06,   172.25, 367.96,  467.73, 2098.82,  88.76,   100.0, 100.0]
    a,b,c=x.fit(years_data,values_data)
    print("a:",a,"b:",b,"c:",c)
    predict = x.predict(a,b,c,50)
    print("predict",predict)
    # print(nihe_error(data['y'].values.tolist(),predict.values.tolist()))
