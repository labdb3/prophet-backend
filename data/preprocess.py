import numpy as np
import pandas as pd
import copy
from matplotlib import pyplot
import xlsxwriter
from common.common import *


def Method1(dataName,window_size):
    fileName,sheetName = getFileName(dataName)
    data = GetDataFrame_dataset(fileName,sheetName,'ds','y').to_numpy().transpose().tolist()

    dataw = []
    if window_size==2:
        model = MovAvg(2)
        dataw = getResult(data[1],model)
    elif window_size==3:
        model = MovAvg(3)
        dataw = getResult(data[1], model)
    elif window_size==4:
        model = MovAvg(4)
        dataw = getResult(data[1], model)
    elif window_size==5:
        model = MovAvg(5)
        dataw = getResult(data[1], model)
    elif window_size==6:
        model = MovAvg(6)
        dataw = getResult(data[1], model)
    elif window_size==7:
        model = MovAvg(7)
        dataw = getResult(data[1], model)
    elif window_size==8:
        model = MovAvg(8)
        dataw = getResult(data[1], model)
    return [data[0],dataw]


def Method2(dataName,window_size):
    data = dataName
    dataw = []
    if window_size==2:
        model = MovAvg(2)
        dataw = getResult(data[1],model)
    elif window_size==3:
        model = MovAvg(3)
        dataw = getResult(data[1], model)
    elif window_size==4:
        model = MovAvg(4)
        dataw = getResult(data[1], model)
    elif window_size==5:
        model = MovAvg(5)
        dataw = getResult(data[1], model)
    elif window_size==6:
        model = MovAvg(6)
        dataw = getResult(data[1], model)
    elif window_size==7:
        model = MovAvg(7)
        dataw = getResult(data[1], model)
    elif window_size==8:
        model = MovAvg(8)
        dataw = getResult(data[1], model)
    return [data[0],dataw]





class MovAvg(object):
    def __init__(self, window_size=7):
        self.window_size = window_size
        self.data_queue = []

    def update(self, data):
        if len(self.data_queue) == self.window_size:
            del self.data_queue[0]
        self.data_queue.append(data)
        return sum(self.data_queue)/len(self.data_queue)

def getResult(data,model):
    data_list = []
    for item in data:
        data_list.append(model.update(item))

    sum1 = sum(data)
    sum2 = sum(data_list)
    for i in range(len(data_list)):
        data_list[i]=data_list[i]/sum2 * sum1
    return data_list
