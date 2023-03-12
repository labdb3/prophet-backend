from common.common import *

'''
@:param dataName: 数据名称，例如,数据单元1
@:param: window_size: 窗口大小
'''


def Method1(dataName,window_size):
    fileName,sheetName = getFileName(dataName)
    data = GetDataFrame_dataset(fileName,sheetName,'ds','y').to_numpy().transpose().tolist()
    dataw = []
    if 2 <= window_size <= 8:
        model = MovAvg(window_size)
        dataw = getResult(data[1], model)
    return [data[0],dataw]


def Method2(data,window_size):
    dataw = []
    if 2 <= window_size <= 8:
        model = MovAvg(window_size)
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
