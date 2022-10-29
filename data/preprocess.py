import pandas as pd
import copy
from matplotlib import pyplot
import xlsxwriter
from common.common import *

def get_sum(data):
    data1 = copy.deepcopy(data)
    ll = len(data1)
    s = 0
    for i in range(ll):
        s = s + data['y'].values[i]
        data1['y'].values[i] = s
    return data1

def slide_window2(data,x1,x2):
    data1 = copy.deepcopy(data)
    ll = len(data1)
    m = 0
    for i in range(ll):
        if data1['y'].values[i] == 1:
            data1['y'].values[i] = 0
    for i in range(ll):
        if data1['y'].values[i] > 0:
            m = data1['y'].values[i]
            break
    for i in range(ll):
        if data1['y'].values[i] < m and data1['y'].values[i] > 0:
            m = data1['y'].values[i]
    zb = 0
    dm = m / 4
    if dm <= 1:
        dm = m
    for i in range(ll):
        if data1['y'].values[i] == 0.0:
            data1['y'].values[i] = dm
            zb += dm
    for i in range(1, len(data1) ):
        s0 = data1['y'].values[i - 1] + data1['y'].values[i]
        data1['y'].values[i] = (x1 * data1['y'].values[i-1] + x2*data1['y'].values[i ] ) / (x1+x2)
        s1 = data1['y'].values[i - 1] + data1['y'].values[i]
        s = s0 - s1
        data1['y'].values[i - 1] += (data1['y'].values[i - 1] / s1) * s
        data1['y'].values[i] += (data1['y'].values[i] / s1) * s
    sum = 0
    for i in range(ll):
        sum += data1['y'].values[i]
    for i in range(ll):
        data1['y'].values[i] = data1['y'].values[i] - zb * (data1['y'].values[i] / sum)
    return data1

def slide_window3(data,M,L,R):
    data1 = copy.deepcopy(data)
    ll = len(data1)
    m = 0
    for i in range(ll):
        if data1['y'].values[i] == 1:
            data1['y'].values[i] = 0
    for i in range(ll):
        if data1['y'].values[i] > 0:
            m = data1['y'].values[i]
            break
    for i in range(ll):
        if data1['y'].values[i] < m and data1['y'].values[i] > 0:
            m = data1['y'].values[i]
    zb = 0
    dm = m / 4
    if dm <= 1:
        dm = m
    for i in range(ll):
        if data1['y'].values[i] == 0.0:
            data1['y'].values[i] = dm
            zb += dm
    for i in range(1, len(data1) - 1):
        s0 = data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]
        data1['y'].values[i] = (M * data1['y'].values[i] + L*data1['y'].values[i - 1] + R*data1['y'].values[
            i + 1]) / (M+L+R)
        s1 = data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]
        s = s0 - s1
        data1['y'].values[i - 1] += (data1['y'].values[i - 1] / s1) * s
        data1['y'].values[i] += (data1['y'].values[i] / s1) * s
        data1['y'].values[i + 1] += (data1['y'].values[i + 1] / s1) * s

    sum = 0
    for i in range(ll):
        sum += data1['y'].values[i]
    for i in range(ll):
        data1['y'].values[i] = data1['y'].values[i] - zb * (data1['y'].values[i] / sum)
    return data1

def slide_window4(data,x1,x2,x3,x4):
    data1 = copy.deepcopy(data)
    ll = len(data1)
    m = 0
    for i in range(ll):
        if data1['y'].values[i] == 1:
            data1['y'].values[i] = 0
    for i in range(ll):
        if data1['y'].values[i] > 0:
            m = data1['y'].values[i]
            break
    for i in range(ll):
        if data1['y'].values[i] < m and data1['y'].values[i] > 0:
            m = data1['y'].values[i]
    zb = 0
    dm = m / 4
    if dm <= 1:
        dm = m
    for i in range(ll):
        if data1['y'].values[i] == 0.0:
            data1['y'].values[i] = dm
            zb += dm
    for i in range(2, len(data1) - 1):
        s0 = data1['y'].values[i - 2] + data1['y'].values[i-1] + data1['y'].values[i ]+data1['y'].values[i + 1]
        x=(x1+x2+x3+x4)
        data1['y'].values[i] = (x1 * data1['y'].values[i-2] + x2*data1['y'].values[i - 1] + x3*data1['y'].values[i ]+x4*data1['y'].values[
            i + 1]) / x
        s1 = data1['y'].values[i - 2]+data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]
        s = s0 - s1
        data1['y'].values[i - 2] += (data1['y'].values[i - 2] / s1) * s
        data1['y'].values[i - 1] += (data1['y'].values[i - 1] / s1) * s
        data1['y'].values[i] += (data1['y'].values[i] / s1) * s
        data1['y'].values[i + 1] += (data1['y'].values[i + 1] / s1) * s

    sum = 0
    for i in range(ll):
        sum += data1['y'].values[i]
    for i in range(ll):
        data1['y'].values[i] = data1['y'].values[i] - zb * (data1['y'].values[i] / sum)
    return data1

def slide_window5(data,x1,x2,x3,x4,x5):
    data1 = copy.deepcopy(data)
    ll = len(data1)
    m = 0
    for i in range(ll):
        if data1['y'].values[i] == 1:
            data1['y'].values[i] = 0
    for i in range(ll):
        if data1['y'].values[i] > 0:
            m = data1['y'].values[i]
            break
    for i in range(ll):
        if data1['y'].values[i] < m and data1['y'].values[i] > 0:
            m = data1['y'].values[i]
    zb = 0
    dm = m / 4
    if dm <= 1:
        dm = m
    for i in range(ll):
        if data1['y'].values[i] == 0.0:
            data1['y'].values[i] = dm
            zb += dm
    for i in range(2, len(data1) - 2):
        s0 = data1['y'].values[i - 2] + data1['y'].values[i-1] + data1['y'].values[i ]+data1['y'].values[i + 1]+data1['y'].values[i + 2]
        x=(x1+x2+x3+x4+x5)
        data1['y'].values[i] = (x1 * data1['y'].values[i-2] + x2*data1['y'].values[i - 1] + x3*data1['y'].values[i ]+x4*data1['y'].values[
            i + 1]+x5 * data1['y'].values[i+2]) / x
        s1 = data1['y'].values[i - 2]+data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]+ data1['y'].values[i + 2]
        s = s0 - s1
        data1['y'].values[i - 2] += (data1['y'].values[i - 2] / s1) * s
        data1['y'].values[i - 1] += (data1['y'].values[i - 1] / s1) * s
        data1['y'].values[i] += (data1['y'].values[i] / s1) * s
        data1['y'].values[i + 1] += (data1['y'].values[i + 1] / s1) * s
        data1['y'].values[i + 2] += (data1['y'].values[i + 2] / s1) * s

    sum = 0
    for i in range(ll):
        sum += data1['y'].values[i]
    for i in range(ll):
        data1['y'].values[i] = data1['y'].values[i] - zb * (data1['y'].values[i] / sum)
    return data1

def slide_window6(data,x1,x2,x3,x4,x5,x6):
    data1 = copy.deepcopy(data)
    ll = len(data1)
    m = 0
    for i in range(ll):
        if data1['y'].values[i] == 1:
            data1['y'].values[i] = 0
    for i in range(ll):
        if data1['y'].values[i] > 0:
            m = data1['y'].values[i]
            break
    for i in range(ll):
        if data1['y'].values[i] < m and data1['y'].values[i] > 0:
            m = data1['y'].values[i]
    zb = 0
    dm = m / 4
    if dm <= 1:
        dm = m
    for i in range(ll):
        if data1['y'].values[i] == 0.0:
            data1['y'].values[i] = dm
            zb += dm
    for i in range(3, len(data1) - 2):
        s0 = data1['y'].values[i - 3] +data1['y'].values[i - 2] + data1['y'].values[i-1] + data1['y'].values[i ]+data1['y'].values[i + 1]+data1['y'].values[i + 2]
        x=(x1+x2+x3+x4+x5+x6)
        data1['y'].values[i] = (x1 * data1['y'].values[i-3] +x2 * data1['y'].values[i-2] + x3*data1['y'].values[i - 1] + x4*data1['y'].values[i ]+x5*data1['y'].values[
            i + 1]+x6 * data1['y'].values[i+2]) / x
        s1 =data1['y'].values[i - 3]+ data1['y'].values[i - 2]+data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]+ data1['y'].values[i + 2]
        s = s0 - s1
        data1['y'].values[i - 3] += (data1['y'].values[i - 3] / s1) * s
        data1['y'].values[i - 2] += (data1['y'].values[i - 2] / s1) * s
        data1['y'].values[i - 1] += (data1['y'].values[i - 1] / s1) * s
        data1['y'].values[i] += (data1['y'].values[i] / s1) * s
        data1['y'].values[i + 1] += (data1['y'].values[i + 1] / s1) * s
        data1['y'].values[i + 2] += (data1['y'].values[i + 2] / s1) * s

    sum = 0
    for i in range(ll):
        sum += data1['y'].values[i]
    for i in range(ll):
        data1['y'].values[i] = data1['y'].values[i] - zb * (data1['y'].values[i] / sum)
    return data1

def slide_window7(data,x1,x2,x3,x4,x5,x6,x7):
    data1 = copy.deepcopy(data)
    ll = len(data1)
    m = 0
    for i in range(ll):
        if data1['y'].values[i] == 1:
            data1['y'].values[i] = 0
    for i in range(ll):
        if data1['y'].values[i] > 0:
            m = data1['y'].values[i]
            break
    for i in range(ll):
        if data1['y'].values[i] < m and data1['y'].values[i] > 0:
            m = data1['y'].values[i]
    zb = 0
    dm = m / 4
    if dm <= 1:
        dm = m
    for i in range(ll):
        if data1['y'].values[i] == 0.0:
            data1['y'].values[i] = dm
            zb += dm
    for i in range(3, len(data1) - 3):
        s0 = data1['y'].values[i - 3] +data1['y'].values[i - 2] + data1['y'].values[i-1] + data1['y'].values[i]\
             +data1['y'].values[i + 1]+data1['y'].values[i + 2]+data1['y'].values[i + 3]
        x=(x1+x2+x3+x4+x5+x6+x7)
        data1['y'].values[i] = (x1 * data1['y'].values[i-3] +x2 * data1['y'].values[i-2] + x3*data1['y'].values[i - 1] + x4*data1['y'].values[i ]+x5*data1['y'].values[
            i + 1]+x6 * data1['y'].values[i+2]+x7 * data1['y'].values[i+3]) / x
        s1 =data1['y'].values[i - 3]+ data1['y'].values[i - 2]+data1['y'].values[i - 1] + data1['y'].values[i] \
            + data1['y'].values[i + 1]+ data1['y'].values[i + 2]+ data1['y'].values[i + 3]
        s = s0 - s1
        data1['y'].values[i - 3] += (data1['y'].values[i - 3] / s1) * s
        data1['y'].values[i - 2] += (data1['y'].values[i - 2] / s1) * s
        data1['y'].values[i - 1] += (data1['y'].values[i - 1] / s1) * s
        data1['y'].values[i] += (data1['y'].values[i] / s1) * s
        data1['y'].values[i + 1] += (data1['y'].values[i + 1] / s1) * s
        data1['y'].values[i + 2] += (data1['y'].values[i + 2] / s1) * s
        data1['y'].values[i + 3] += (data1['y'].values[i + 3] / s1) * s

    sum = 0
    for i in range(ll):
        sum += data1['y'].values[i]
    for i in range(ll):
        data1['y'].values[i] = data1['y'].values[i] - zb * (data1['y'].values[i] / sum)
    return data1

def slide_window8(data,x1,x2,x3,x4,x5,x6,x7,x8):
    data1 = copy.deepcopy(data)
    ll = len(data1)
    m = 0
    for i in range(ll):
        if data1['y'].values[i] == 1:
            data1['y'].values[i] = 0
    for i in range(ll):
        if data1['y'].values[i] > 0:
            m = data1['y'].values[i]
            break
    for i in range(ll):
        if data1['y'].values[i] < m and data1['y'].values[i] > 0:
            m = data1['y'].values[i]
    zb = 0
    dm = m / 4
    if dm <= 1:
        dm = m
    for i in range(ll):
        if data1['y'].values[i] == 0.0:
            data1['y'].values[i] = dm
            zb += dm
    for i in range(4, len(data1) - 3):
        s0 =data1['y'].values[i - 4] + data1['y'].values[i - 3] +data1['y'].values[i - 2] + data1['y'].values[i-1] + data1['y'].values[i]\
             +data1['y'].values[i + 1]+data1['y'].values[i + 2]+data1['y'].values[i + 3]
        x=(x1+x2+x3+x4+x5+x6+x7+x8)
        data1['y'].values[i] = (x1 * data1['y'].values[i-4] +x2 * data1['y'].values[i-3] +x3 * data1['y'].values[i-2] + x4*data1['y'].values[i - 1] + x5*data1['y'].values[i ]+x6*data1['y'].values[
            i + 1]+x7 * data1['y'].values[i+2]+x8 * data1['y'].values[i+3]) / x
        s1 =data1['y'].values[i - 4]+data1['y'].values[i - 3]+ data1['y'].values[i - 2]+data1['y'].values[i - 1] + data1['y'].values[i] \
            + data1['y'].values[i + 1]+ data1['y'].values[i + 2]+ data1['y'].values[i + 3]
        s = s0 - s1
        data1['y'].values[i - 4] += (data1['y'].values[i - 4] / s1) * s
        data1['y'].values[i - 3] += (data1['y'].values[i - 3] / s1) * s
        data1['y'].values[i - 2] += (data1['y'].values[i - 2] / s1) * s
        data1['y'].values[i - 1] += (data1['y'].values[i - 1] / s1) * s
        data1['y'].values[i] += (data1['y'].values[i] / s1) * s
        data1['y'].values[i + 1] += (data1['y'].values[i + 1] / s1) * s
        data1['y'].values[i + 2] += (data1['y'].values[i + 2] / s1) * s
        data1['y'].values[i + 3] += (data1['y'].values[i + 3] / s1) * s

    sum = 0
    for i in range(ll):
        sum += data1['y'].values[i]
    for i in range(ll):
        data1['y'].values[i] = data1['y'].values[i] - zb * (data1['y'].values[i] / sum)
    return data1


# dataw = slide_window(data,6,0.85,1.15)
#
# print(data)
# print(dataw)
# #
# workbook = xlsxwriter.Workbook('sheet1.xlsx')
# worksheet = workbook.add_worksheet()
# for i in range(len(dataw)):
#     worksheet.write(i, 0, dataw['ds'].values[i])
#     worksheet.write(i, 1, dataw['y'].values[i])
# workbook.close()
# print("dataw", dataw)
# yw = dataw['y'].values
# y0 = data['y'].values
# y0 = copy.deepcopy(y0)
# x1 = [i for i in range(len(data))]
#
# # print(y0)
# pyplot.plot(x1, y0, label='INITIALLY')
# # pyplot.plot(x1, y1, label='PREPROC1')
# # pyplot.plot(x1, y2, label='WS=3')
# pyplot.plot(x1, yw, label='W')
# # pyplot.plot(x1, y3, label='WS=5')
# pyplot.title("log_sample1 new")
# pyplot.legend()
# pyplot.show()
# print('datasum', get_sum(data))
# print('datawsum', get_sum(dataw))



def Method1(dataName,window_size):
    fileName,sheetName = getFileName(dataName)
    data = GetDataFrame_dataset(fileName,sheetName,'ds','y')
    data.columns = ['ds', 'y']

    if window_size==2:
        dataw =  slide_window2(data,1,1)
    elif window_size==3:
        dataw = slide_window3(data, 1, 1, 1)
    elif window_size==4:
        dataw = slide_window4(data, 1, 1, 1, 1)
    elif window_size==5:
        dataw = slide_window5(data, 1, 1, 1, 1, 1)
    elif window_size==6:
        dataw = slide_window6(data, 1, 1, 1, 1, 1, 1)
    elif window_size==7:
        dataw = slide_window7(data, 1, 1, 1, 1, 1, 1, 1)
    elif window_size==8:
        dataw = slide_window8(data, 1, 1, 1, 1, 1, 1, 1, 1)
    return dataw.to_numpy().transpose().tolist()
