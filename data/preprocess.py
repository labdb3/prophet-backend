import pandas as pd
import copy
import os
from matplotlib import pyplot
import xlsxwriter

#BASE_DIR = '/Users/zongdianliu/python/prophet-backend/data/datasets'
BASE_DIR = 'D:\dblab3\prophet-backend\data\datasets'

def preprocess(data):
    i = 0
    while (i < (len(data['y'].values) - 2)):
        if data['y'].values[i] == 0 or data['y'].values[i] == 1:
            temp = i
            while (data['y'].values[i + 1] == 0 or data['y'].values[i + 1] == 1):
                i += 1
            if temp == i:
                if i == 0:
                    data['y'].values[0] = 2 / 5 * data['y'].values[1]
                    data['y'].values[1] = 3 / 5 * data['y'].values[1]
                elif i == len(data['y'].values) - 1:
                    data['y'].values[i] = 2 / 5 * data['y'].values[i - 1]
                    data['y'].values[i - 1] = 3 / 5 * data['y'].values[i - 1]
                else:
                    if data['y'].values[i - 1] > data['y'].values[i + 1]:
                        data['y'].values[i + 1] = (data['y'].values[i - 1] + data['y'].values[i + 1]) / 3 - (
                                data['y'].values[i - 1] - data['y'].values[i + 1]) / 6
                        data['y'].values[i] = (data['y'].values[i - 1] + data['y'].values[i + 1]) / 3
                        data['y'].values[i - 1] = (data['y'].values[i - 1] + data['y'].values[i + 1]) / 3 + (
                                data['y'].values[i - 1] - data['y'].values[i + 1]) / 6
                    elif data['y'].values[i - 1] <= data['y'].values[i + 1]:
                        data['y'].values[i + 1] = (data['y'].values[i - 1] + data['y'].values[i + 1]) / 3 + (
                                data['y'].values[i + 1] - data['y'].values[i - 1]) / 6
                        data['y'].values[i] = (data['y'].values[i - 1] + data['y'].values[i + 1]) / 3
                        data['y'].values[i - 1] = (data['y'].values[i - 1] + data['y'].values[i + 1]) / 3 - (
                                data['y'].values[i + 1] - data['y'].values[i - 1]) / 6
            elif temp != i:
                if temp == 0:
                    data['y'].values[temp] = (data['y'].values[i + 1] - (i - temp + 2) * data['y'].values[
                        i + 1] / 6) / (i - temp + 2)
                    for j in range(temp + 1, i + 2):
                        data['y'].values[j] = data['y'].values[temp] + (j - temp) * data['y'].values[i + 1] / (
                                i - temp + 1) / 3
                elif i == len(data['y'].values) - 1:
                    data['y'].values[i] = (data['y'].values[temp - 1] - (i - temp + 2) * data['y'].values[
                        temp - 1] / 6) / (i - temp + 2)
                    for j in range(temp - 1, i):
                        data['y'].values[j] = data['y'].values[i] + (i - j) * data['y'].values[temp - 1] / (
                                i - temp + 1) / 3
                else:
                    if data['y'].values[temp - 1] > data['y'].values[i + 1]:
                        data['y'].values[i + 1] = (data['y'].values[temp - 1] + data['y'].values[i + 1] - (
                                i - temp + 3) * (data['y'].values[temp - 1] - data['y'].values[i + 1]) / 6) / (
                                                          i - temp + 3)

                        for j in range(temp - 1, i + 1):
                            data['y'].values[j] = data['y'].values[i + 1] + (i + 1 - j) * (
                                    data['y'].values[temp - 1] - data['y'].values[i + 1]) / 3 / (i - temp + 2)
                    elif data['y'].values[temp - 1] <= data['y'].values[i + 1]:
                        data['y'].values[temp - 1] = (data['y'].values[temp - 1] + data['y'].values[i + 1] - (
                                i - temp + 3) * (data['y'].values[i + 1] - data['y'].values[temp - 1]) / 6) / (
                                                             i - temp + 3)
                        for j in range(temp, i + 2):
                            data['y'].values[j] = data['y'].values[temp - 1] + (j - temp + 1) * (
                                    data['y'].values[i + 1] - data['y'].values[temp - 1]) / 3 / (i - temp + 2)
        i += 1
    return data


def get_sum(data):
    data1 = copy.deepcopy(data)
    ll = len(data1)
    s = 0
    for i in range(ll):
        s = s + data['y'].values[i]
        data1['y'].values[i] = s
    return data1


def slide_window(data, half):
    data1 = copy.deepcopy(data)
    winsize = half * 2 + 1
    sum = 0
    for i in range(winsize):
        sum += data['y'].values[i]
    j1 = 0
    j2 = winsize
    for i in range(half, len(data) - half):
        data1['y'].values[i] = sum / winsize
        if j2 < len(data):
            sum = sum - data['y'].values[j1] + data['y'].values[j2]
        j1 = j1 + 1
        j2 = j2 + 1
    s1 = 0
    s2 = 0
    for i in range(len(data)):
        s1 += data['y'].values[i]
    for i in range(len(data1)):
        s2 += data1['y'].values[i]
    q = (s1 - s2) / len(data1)
    flag = False
    for i in range(len(data1)):
        data1['y'].values[i] += q
        if data1['y'].values[i] <= 1:
            flag = True
    if flag == False:
        return data1
    else:
        return data

def slide_window0(data):
    data1 = copy.deepcopy(data)
    ll = len(data1)
    m = 0
    for i in range(ll):
        if data1['y'].values[i] == 1:
            data1['y'].values[i] = 0
    data2 = copy.deepcopy(data1)
    for i in range(ll):
        if data1['y'].values[i] > 0:
            m = data1['y'].values[i]
            break
    for i in range(ll):
        if data1['y'].values[i] < m and data1['y'].values[i] > 0:
            m = data1['y'].values[i]
    dm = m / 4
    if dm <= 1:
        dm = m
    for i in range(ll):
        if data1['y'].values[i] == 0.0:
            data1['y'].values[i] = dm
    for i in range(1, len(data1) - 1):
        data1['y'].values[i] = (4*data2['y'].values[i] + data2['y'].values[i - 1] + data2['y'].values[
            i + 1]) / 6
    s1 = 0
    s2 = 0
    for i in range(len(data2)):
        s1 += data2['y'].values[i]
    for i in range(len(data1)):
        s2 += data1['y'].values[i]
    s = s1 - s2
    for i in range(ll):
        data1['y'].values[i] = data1['y'].values[i] + s * (data1['y'].values[i] / s2)
    return data1

def slide_window1(data):
    data1 = copy.deepcopy(data)
    ll = len(data1)
    m = 0
    for i in range(ll):
        if data1['y'].values[i] == 1:
            data1['y'].values[i] = 0
    data2 = copy.deepcopy(data1)
    for i in range(ll):
        if data1['y'].values[i] > 0:
            m = data1['y'].values[i]
            break
    for i in range(ll):
        if data1['y'].values[i] < m and data1['y'].values[i] > 0:
            m = data1['y'].values[i]
    dm = m / 4
    if dm <= 1:
        dm = m
    for i in range(ll):
        if data1['y'].values[i] == 0.0:
            data1['y'].values[i] = dm
    for i in range(1, len(data1) - 1):
        data1['y'].values[i] = (data2['y'].values[i] + data2['y'].values[i - 1] + data2['y'].values[
            i + 1]) / 3
    s1 = 0
    s2 = 0
    for i in range(len(data2)):
        s1 += data2['y'].values[i]
    for i in range(len(data1)):
        s2 += data1['y'].values[i]
    s = s1 - s2
    for i in range(ll):
        data1['y'].values[i] = data1['y'].values[i] + s * (data1['y'].values[i] / s2)
    return data1

def slide_window15(data):
    data1 = copy.deepcopy(data)
    ll = len(data1)
    m = 0
    for i in range(ll):
        if data1['y'].values[i] == 1:
            data1['y'].values[i] = 0
    data2 = copy.deepcopy(data1)
    for i in range(ll):
        if data1['y'].values[i] > 0:
            m = data1['y'].values[i]
            break
    for i in range(ll):
        if data1['y'].values[i] < m and data1['y'].values[i] > 0:
            m = data1['y'].values[i]
    dm = m / 4
    if dm <= 1:
        dm = m
    for i in range(ll):
        if data1['y'].values[i] == 0.0:
            data1['y'].values[i] = dm
    for i in range(2, len(data1) - 2):
        data1['y'].values[i] = (data2['y'].values[i] + data2['y'].values[i - 1] + data2['y'].values[
            i + 1]+data2['y'].values[i - 2] + data2['y'].values[
            i + 2]) / 3
    s1 = 0
    s2 = 0
    for i in range(len(data2)):
        s1 += data2['y'].values[i]
    for i in range(len(data1)):
        s2 += data1['y'].values[i]
    s = s1 - s2
    for i in range(ll):
        data1['y'].values[i] = data1['y'].values[i] + s * (data1['y'].values[i] / s2)
    return data1


def slide_window2(data):
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
    print("dm", dm)
    print('n7', data1['y'].values[7])
    for i in range(ll):
        if data1['y'].values[i] == 0.0:
            data1['y'].values[i] = dm
            zb += dm
    for i in range(1, len(data1) - 1):
        s0 = data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]
        data1['y'].values[i] = (6 * data1['y'].values[i] + 0.85*data1['y'].values[i - 1] + 1.15*data1['y'].values[
            i + 1]) / 8
        s1 = data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]
        s = s0 - s1
        data1['y'].values[i - 1] += (data1['y'].values[i - 1] / s1) * s
        data1['y'].values[i] += (data1['y'].values[i] / s1) * s
        data1['y'].values[i + 1] += (data1['y'].values[i + 1] / s1) * s
 #   for j in range(1, len(data1) - 1):
 #       i = len(data1) - 1 - j
  #      s0 = data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]
 #       data1['y'].values[i] = (6 * data1['y'].values[i] + 0.85 * data1['y'].values[i - 1] + 1.15 * data1['y'].values[
 #           i + 1]) / 8
 #       s1 = data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]
 #       s = s0 - s1
 #       data1['y'].values[i - 1] += (data1['y'].values[i - 1] / s1) * s
 #       data1['y'].values[i] += (data1['y'].values[i] / s1) * s
  #      data1['y'].values[i + 1] += (data1['y'].values[i + 1] / s1) * s

    sum = 0
    for i in range(ll):
        sum += data1['y'].values[i]
    for i in range(ll):
        data1['y'].values[i] = data1['y'].values[i] - zb * (data1['y'].values[i] / sum)
    return data1


def slide_window3(data):
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
    print("dm", dm)
    print('n7', data1['y'].values[7])
    for i in range(ll):
        if data1['y'].values[i] == 0.0:
            data1['y'].values[i] = dm
            zb += dm
    for i in range(1, len(data1) - 1):
        s0 = data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]
        data1['y'].values[i] = (2 * data1['y'].values[i] + data1['y'].values[i - 1] + data1['y'].values[
            i + 1]) / 4
        s1 = data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]
        s = s0 - s1
        data1['y'].values[i - 1] += (data1['y'].values[i - 1] / s1) * s
        data1['y'].values[i] += (data1['y'].values[i] / s1) * s
        data1['y'].values[i + 1] += (data1['y'].values[i + 1] / s1) * s
    for j in range(1, len(data1) - 1):
        i = len(data1) - 1 - j
        s0 = data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]
        data1['y'].values[i] = (2* data1['y'].values[i] + 0.85 * data1['y'].values[i - 1] + 1.15 * data1['y'].values[
            i + 1]) / 4
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


def slide_window4(data):
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
    print("dm", dm)
    print('n7', data1['y'].values[7])
    for i in range(ll):
        if data1['y'].values[i] == 0.0:
            data1['y'].values[i] = dm
            zb += dm
    for i in range(1, len(data1) - 1):
        s0 = data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]
        data1['y'].values[i] = ( data1['y'].values[i] + data1['y'].values[i - 1] + data1['y'].values[
            i + 1]) / 3
        s1 = data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]
        s = s0 - s1
        data1['y'].values[i - 1] += (data1['y'].values[i - 1] / s1) * s
        data1['y'].values[i] += (data1['y'].values[i] / s1) * s
        data1['y'].values[i + 1] += (data1['y'].values[i + 1] / s1) * s
    for j in range(1, len(data1) - 1):
        i = len(data1) - 1 - j
        s0 = data1['y'].values[i - 1] + data1['y'].values[i] + data1['y'].values[i + 1]
        data1['y'].values[i] = ( data1['y'].values[i] +  data1['y'].values[i - 1] +  data1['y'].values[
            i + 1]) / 3
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

def slide_window(data,M,L,R):
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
    ##print("dm", dm)
    ##print('n7', data1['y'].values[7])
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




def getFileName(query):
    fileName = None
    for file in os.listdir(BASE_DIR):
        if file.split(".")[0] == query.split("_")[0]:
            fileName = file
            break


    return [fileName,query.split("_")[1]]



def Method1(dataName):
    fileName, sheetName = getFileName(dataName)
    data = pd.read_excel(os.path.join(BASE_DIR, fileName), header=0, skiprows=0,
                         sheet_name=sheetName)

    data.columns = ['ds', 'y']
    dataw = slide_window(data, 6, 0.85, 1.15)
    return dataw.to_numpy().transpose().tolist()
