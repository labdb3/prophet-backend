import pandas as pd
import numpy as np


def preprocess(data):
    '''
    :description:数据缺失值处理算法
    这个邦彦师兄他的代码风格实在是一言难尽，我就不改了......
    :param data:
    :return:处理好的数据 仍是dataframe格式
    '''
    ##data.columns = ['ds','y']
    i = 0
    while (i<(len(data['y'].values)-2)):
        if data['y'].values[i]==0 or data['y'].values[i]==1:
            temp = i
            while(data['y'].values[i+1]==0 or data['y'].values[i+1]==1):
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


def pre_process_with_list(data):
    data = pd.DataFrame(np.array(data).reshape((-1, 1)))
    data.columns = ['y']
    i = 0
    while (i < (len(data['y'].values) - 2)):
        if data['y'].values[i] == 0 or data['y'].values[i] == 1:
            temp = i
            while (data['y'].values[i + 1] == 0 or data['y'].values[i + 1] == 1):
                i += 1
            if temp == i:
                if i == 0:
                    data['y'].values[0] = 2 / 5 * data['y'].values[1]
                    print(data['y'].values[0])
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
    return data.to_numpy().transpose().tolist()[0]
