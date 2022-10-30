import pandas as pd


def preprocess(data):
    '''
    :description : 邦彦师兄的数据预处理方法，思想是将异常值与临近值按照等差数列进行处理，维持总量不变
    :param data: a pandas dataframe
    :return: pandas dataframe after preprocessing
    '''
    data.columns = ['ds', 'y']
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
    ###如果你对列有自己的命名方式，不要忘了改回去^_^
    return data


def sliding_window(data, middle_weight, left_weight, right_weight):
    '''
    description: 亚伦师弟的利用滑动窗口进行平滑处理的方法
    :param data: pandas data frame
    :param middle_weight:
    :param left_weight:
    :param right_weight:
    :return: data frame after preprocessing
    a recommendation for parameters: [data, 6, 0.85, 1.15]
    '''
    data.columns = ['ds', 'y']
    ll = len(data)
    m = 0
    for i in range(ll):
        if data['y'].values[i] == 1:
            data['y'].values[i] = 0
    for i in range(ll):
        if data['y'].values[i] > 0:
            m = data['y'].values[i]
            break
    for i in range(ll):
        if data['y'].values[i] < m and data['y'].values[i] > 0:
            m = data['y'].values[i]
    zb = 0
    dm = m / 4
    if dm <= 1:
        dm = m
    ##print("dm", dm)
    ##print('n7', data1['y'].values[7])
    for i in range(ll):
        if data['y'].values[i] == 0.0:
            data['y'].values[i] = dm
            zb += dm
    for i in range(1, len(data) - 1):
        s0 = data['y'].values[i - 1] + data['y'].values[i] + data['y'].values[i + 1]
        data['y'].values[i] = (middle_weight * data['y'].values[i] + left_weight * data['y'].values[i - 1] + right_weight * data['y'].values[
            i + 1]) / (middle_weight + left_weight + right_weight)
        s1 = data['y'].values[i - 1] + data['y'].values[i] + data['y'].values[i + 1]
        s = s0 - s1
        data['y'].values[i - 1] += (data['y'].values[i - 1] / s1) * s
        data['y'].values[i] += (data['y'].values[i] / s1) * s
        data['y'].values[i + 1] += (data['y'].values[i + 1] / s1) * s

    sum = 0
    for i in range(ll):
        sum += data['y'].values[i]
    for i in range(ll):
        data['y'].values[i] = data['y'].values[i] - zb * (data['y'].values[i] / sum)
    ###如果你对列有自己的命名方式，不要忘了改回去^_^
    return data



