from model.model import prophetModel, GMModel,wenshiModel
from model import myGM as data_preprocess
import os
import pandas as pd
from prophet import Prophet
import model.myGM.data_preprocess as data_preprocess
from .util import *
import pickle
import json
from common.common import *
import model.sum.sum_partition as sum_partition
from model.sum.sum_partition import res_list, cur_list


# 默认参数的模型
def getResultOfDataset_prophet(dataset):
    data = GetData(dataset)
    model = prophetModel()
    model.fit(data[0], data[1])
    predict = model.predict(data[0][0], len(data[0]), 0)
    return predict.to_numpy().tolist()


def getResultOfDataset_wensi(dataset):
    data = GetData(dataset)
    model = wenshiModel()
    tmp_x = list(range(1, len(data[0]) + 1))
    tmp_y = data[1]
    model.fit(tmp_x,tmp_y)
    pred_y = model.predict(len(data[0]))
    return pred_y


def getResultOfDataset_GM(dataset):
    x = GMModel()
    fileName, sheetName = getFileName(dataset)
    data = GetDataFrame_dataset(fileName, sheetName, "ds", "y")
    predict_data, predict_res, message = x.predict(data, 5)
    if message:
       return [item[1] for item in predict_res],None
    else:
        return [], "所选参数在计算时矩阵计算时会出现奇异矩阵，请重新选定参数"


# 自定义参数的模型

def getResultWithParams_prophet(dataset,params):
    data = GetData(dataset)

    # print("params",params)
    if params["k"]==0 or params["k"]==None:
        model = prophetModel(params["n_changepoints"],params["changepoint_prior_scale"],params["seasonality_prior_scale"],"log")
        k = model.fit(data[0], data[1])
    else:
        model = prophetModel(params["n_changepoints"], params["changepoint_prior_scale"],
                             params["seasonality_prior_scale"], "log",k=params["k"])
        k = model.fit(data[0],data[1])
    predict = model.predict(data[0][0], len(data[0]), params["years"])
    return predict.to_numpy().tolist(),k


def getResultWithParams_wensi(dataset,params):
    data = GetData(dataset)

    if params["a"]==0 and params["b"]==0 and params["c"]==0:
        tmp_x = list(range(1, len(data[0]) + 1))
        tmp_y = data[1]
        model = wenshiModel()
        model.fit(tmp_x, tmp_y)
    else:
        # print("当前参数为：", params)
        model = wenshiModel(params["a"],params["b"],params["c"])


    pred_y = model.predict(params["years"]+len(data[0]))
    return pred_y,model.a,model.b,model.c

## origin_data: 文件名
## cur_fit_input: 峰值划定结果
'''
 举例 cur_fit_input = [
[[1966,23.66],[1967, 35.99],[1968,86.22],[1969, 32.33]],
[[1970, 26.67], [1971, 38.89], [1972, 89.27], [1973, 28.35]]
 ]
'''
def getResultWithParams_GM(origin_data,params):
    x = GMModel(nums=params['nums'], peak_rate=params['peak_rate'], option = params['option'])
    fileName, sheetName = getFileName(origin_data)
    data = GetDataFrame_dataset(fileName, sheetName, "ds", "y")
    predict_data, predict_res, message = x.predict(data, params["years"])
    if message:
        return [item[1] for item in predict_res], None
    else:
        return [], "所选参数在计算时矩阵计算时会出现奇异矩阵，请重新选定参数"
    '''
    try:
        predict_data, predict_res, message = x.predict(data, params["years"])
        if message:
           return [item[1] for item in predict_res], None
        else:
            return [], "所选参数在计算时矩阵计算时会出现奇异矩阵，请重新选定参数"
    except:
        return [], "所选参数在计算时矩阵计算时会出现奇异矩阵，请重新选定参数"
    '''

## 得到数据预处理的结果，方便前端进行数据分段
## 返回值：一个数组，按照年份排列，每个元素是[年份,产量]
def get_preprocess_res(dataset):
    fileName, sheetName = getFileName(dataset)
    data = GetDataFrame_dataset(fileName, sheetName, "ds", "y")
    pre = data_preprocess.preprocess(data)
    data = []
    length = len(pre['y'].values)
    for i in range(0, length):
        l = []
        l.append(pre['ds'].values[i])
        l.append(pre['y'].values[i])
        data.append(l)
    return data


def get_sum_fitting(dataset, params):
    '''

    :param dataset: 数据集名称
    :param params: 参数列表
          partition_num: 对于累积曲线划分的段数，建议选择3-4
          degree: 拟合的多项式阶数，建议选择2-4
    :return: x_list: 年份的二维列表, for example 如果有三个划分，会这样返回
    [[1963,1964], [1965, 1966, 1967], [1968, 1969, 1970]]
            y_list: 原始的累积产量列表,格式同上
            fitting_y_list: 拟合的累积产量，格式与x_list相同
            jpg_name: 图片文件名称
    '''
    params = {
        "partition_num":3,
        "degree":3,
    }
    cur_list = []
    res_list = []
    fileName, sheetName = getFileName(dataset)
    data = GetDataFrame_dataset(fileName, sheetName, "ds", "y")
    pre = data_preprocess.preprocess(data)
    sum = sum_partition.get_sum(pre)
    partition = sum_partition.get_partition(input_sum=sum, partition_num=params['partition_num'])
    x_list, y_list, fitting_y_list = sum_partition.partition_fitting(partition, deg=params['degree'])
    sum_name, actual_name = sum_partition.save_plot(dataset, x_list, y_list, fitting_y_list)
    return sum_name, actual_name


