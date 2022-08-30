import numpy as np
import os


BASE_DIR = '/Users/zongdianliu/python/prophet-backend/data/datasets'



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