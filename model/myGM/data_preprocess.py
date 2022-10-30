import pandas as pd
import model.myGM.xlsx_reader as xlsx_reader
import numpy as np
import copy
def preprocess(data):
    data.columns = ['ds','y']
    i = 0
    while (i<(len(data['y'].values)-2)):
        if data['y'].values[i]==0 or data['y'].values[i]==1:
            temp = i
            while(data['y'].values[i+1] == 0 or data['y'].values[i+1]==1):
                i += 1
            if temp == i:
                if i == 0:
                    data['y'].values[0] = 2/5*data['y'].values[1]
                    print(data['y'].values[0])
                    data['y'].values[1] = 3 / 5 * data['y'].values[1]
                elif i == len(data['y'].values)-1:
                    data['y'].values[i] = 2 / 5 * data['y'].values[i-1]
                    data['y'].values[i-1] = 3 / 5 * data['y'].values[i-1]
                else:
                    if data['y'].values[i-1] > data['y'].values[i+1]:
                        data['y'].values[i + 1]= (data['y'].values[i-1]+data['y'].values[i+1])/3 - (data['y'].values[i-1]-data['y'].values[i+1])/6
                        data['y'].values[i]= (data['y'].values[i-1]+data['y'].values[i+1])/3
                        data['y'].values[i - 1]=(data['y'].values[i-1]+data['y'].values[i+1])/3 + (data['y'].values[i-1]-data['y'].values[i+1])/6
                    elif data['y'].values[i-1] <= data['y'].values[i+1]:
                        data['y'].values[i + 1] = (data['y'].values[i-1]+data['y'].values[i+1])/3 + (data['y'].values[i+1]-data['y'].values[i-1])/6
                        data['y'].values[i] = (data['y'].values[i - 1] + data['y'].values[i + 1]) / 3
                        data['y'].values[i - 1] = (data['y'].values[i - 1] + data['y'].values[i + 1]) / 3 - (data['y'].values[i + 1] - data['y'].values[i - 1]) / 6
            elif temp != i:
                if temp == 0:
                    data['y'].values[temp] = (data['y'].values[i+1]-(i-temp+2)*data['y'].values[i+1]/6)/(i-temp+2)
                    for j in range(temp+1,i+2):
                        data['y'].values[j] = data['y'].values[temp]+(j-temp)*data['y'].values[i+1]/(i-temp+1)/3
                elif i == len(data['y'].values)-1:
                    data['y'].values[i] = (data['y'].values[temp-1]-(i-temp+2)*data['y'].values[temp-1]/6)/(i-temp+2)
                    for j in range(temp-1,i):
                        data['y'].values[j] = data['y'].values[i] + (i-j)*data['y'].values[temp-1]/(i-temp+1)/3
                else:
                    if data['y'].values[temp-1] > data['y'].values[i+1]:
                        data['y'].values[i+1] = (data['y'].values[temp - 1]+data['y'].values[i+1]-(i-temp+3)*(data['y'].values[temp-1]-data['y'].values[i+1])/6)/(i-temp+3)

                        for j in range(temp-1,i+1):
                            data['y'].values[j] = data['y'].values[i+1] + (i+1-j)*(data['y'].values[temp-1]-data['y'].values[i+1])/3/(i-temp+2)
                    elif data['y'].values[temp-1] <= data['y'].values[i+1]:
                        data['y'].values[temp - 1] = (data['y'].values[temp - 1]+data['y'].values[i+1]-(i-temp+3)*(data['y'].values[i+1]-data['y'].values[temp-1])/6)/(i-temp+3)
                        for j in range(temp,i+2):
                            data['y'].values[j]= data['y'].values[temp - 1]+(j-temp+1)*(data['y'].values[i+1]-data['y'].values[temp-1])/3/(i-temp+2)
        i += 1
    return data


def get_max_index(data, nums, peak_rate):
    res = []
    i = 0
    while data[i+1][1] < data[i][1] and i < len(data) + 1:
        i += 1
    if i > 0:
        res.append(i)
    while i < len(data):
        flag, idx = is_peak(data, i, peak_rate, nums)
        if not flag:
            i += 1
        else:
            res.append(idx)
            i = idx + 1
    length = len(res)
    if length == 0 or res[length - 1] < len(data) - 1:
        res.append(len(data) - 1)
    return res


def is_peak(data, index, peak_rate, nums, back_trend_rate = 0.15):
    peak_num = data[index][1]
    for i in range(1, nums + 1):
        if index - i <= 0 or index + i >= len(data):
            return False, - 1
        if data[index - i][1] >= data[index - i + 1][1] or data[index + i][1] >= data[index + i - 1][1]:
            return False, - 1
    before = data[index - 1][1]
    after = data[index + 1][1]
    if (peak_num - before)/ peak_num < peak_rate and (peak_num - after)/ peak_num < peak_rate:
        return False, -1
    for i in range(index + nums + 1, len(data)):
        if data[i][1] >= data[i - 1][1] and (data[i][1] - data[i-1][1]/data[i-1][1] >= back_trend_rate):
            return True, i - 1
    return True, len(data) - 1


def get_curve_fit_input(data, end_idx):
    res = []
    start_index = 0
    for e in end_idx:
        end = []
        for j in range(start_index, e+1):
            end.append(data[j])
        if len(end) >0:
            res.append(end)
        start_index = e + 1
    return res

'''
pre = preprocess(data)
##print(pre)
data = []
length = len(pre['y'].values)
for i in range(0, length):
    l = []
    l.append(pre['ds'].values[i])
    l.append(pre['y'].values[i])
    data.append(l)
##print(data)
idx = get_max_index(data)
res = get_curve_fit_input(data, idx)
par = xlsx_reader.cur_fit(res)
par = np.array(par)
temp = copy.deepcopy(par)
model_input, stat = xlsx_reader.normalization(par)
Nm_actual = model_input[:, 0]
Nm_relevant = model_input[:, 1:]
Tm_actual = model_input[:, 1]
Tm_relevant = model_input[:, (0, 2)]
b_actual = model_input[:, 2]
b_relevant = model_input[:, (0, 1)]
b_res = xlsx_reader.GM_predict(b_actual, b_relevant, 'b')
Nm_res = xlsx_reader.GM_predict(Nm_actual, Nm_relevant, 'Nm')
Tm_res = xlsx_reader.GM_predict(Tm_actual, Tm_relevant, 'Tm')
for i in range(0, len(b_res)):
    b_res[i] = b_res[i]*stat[2][1] + stat[2][0]
    Nm_res[i] = Nm_res[i] * stat[0][1] + stat[0][0]
    Tm_res[i] = Tm_res[i] * stat[1][1] + stat[1][0]
actual_production = []
fitting_production = []
for i in range(0, len(res)):
    b_act = temp[i][2]
    N_act = temp[i][0]
    T_act = temp[i][1]
    b_pred = b_res[i]
    N_pred = Nm_res[i]
    for r in res[i]:
        actual_production.append(r[1])
        t = r[0]
        fit = 2*N_pred/(1+np.cosh(b_pred*(t - T_act)))
        fitting_production.append(fit)
xlsx_reader.draw(fitting_production, actual_production)
residuals = []
relevancy = []
max_dif = abs(fitting_production[0] - actual_production[0])
min_dif = abs(fitting_production[0] - actual_production[0])
for i in range(0, len(fitting_production)):
    residual = abs((fitting_production[i] - actual_production[i]) / actual_production[i])
    residuals.append(residual)
    max_dif = max(max_dif,  abs(fitting_production[i] - actual_production[i]))
    min_dif = min(min_dif, abs(fitting_production[i] - actual_production[i]))
print(residuals)
for i in range(0, len(fitting_production)):
    r = (min_dif + 0.5 * max_dif)/((abs(fitting_production[i] - actual_production[i])) + 0.5 * max_dif)
    relevancy.append(r)
mean = sum(residuals) / len(residuals)
m_r = sum(relevancy) / len(residuals)
print(mean)
print(m_r)

if mean <= 0.01:
    print("该数据非常适合灰度模型")
elif mean <= 0.05:
    print("该数据适合灰度模型")
elif mean <= 0.1:
    print("该数据勉强适合灰度模型")
else:
    print("该数据不适合灰度模型")
'''
# print(preprocess(data))