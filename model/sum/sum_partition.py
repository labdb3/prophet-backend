import numpy as np
import copy
import pandas as pd
import data.preprocess_util as data_preprocess
import os
from model.pred import BASE_DIR
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['font.sans-serif'] = ['Simsun']
matplotlib.rcParams['font.size'] = 11

res_list = []
cur_list = []


def get_sum(data_frame):
    data = []
    length = len(data_frame['y'].values)
    for i in range(0, length):
        l = []
        l.append(data_frame['ds'].values[i])
        l.append(data_frame['y'].values[i])
        data.append(l)
    for i in range(1, len(data)):
        data[i][1] += data[i-1][1]
    return data


def dfs(cur_idx, cur_length, n, m):
    ##print(str(cur_length) + " " + str(m))
    if cur_length == m-1:
        ##print(cur_list)
        res_list.append(copy.deepcopy(cur_list))
        return res_list

    for i in range(cur_idx, n):
        cur_list.append(i)
        dfs(i + 1, cur_length + 1, n, m)
        del(cur_list[-1])
    return res_list


def get_partition(input_sum, partition_num):
    '''

    :param input_sum: 累积曲线列表
           partition_num: 划分段数
    :return:
    '''
    length = len(input_sum)
    print(length)

    years = [input_sum[i][0] for i in range(0, length)]
    value_sum = [input_sum[i][1] for i in range(0, length)]
    prefix_sum = np.zeros(length)
    prefix_sum[0] = value_sum[0]
    square_prefix_sum = np.zeros(length)
    square_prefix_sum[0] = value_sum[0] * value_sum[0]
    for i in range(1, length):
        prefix_sum[i] = prefix_sum[i-1] + value_sum[i]
        square_prefix_sum[i] = square_prefix_sum[i-1] + value_sum[i]* value_sum[i]
    res_list = []
    cur_list = []
    res_list = dfs(cur_idx=0, cur_length=0, n=length - 1, m=partition_num)
    min_diff = 1e11
    min_partition_plan = []
    for partition_plan in res_list:
        curr_diff = 0e0
        prev_idx = -1
        for num in partition_plan:
            curr_expectation = (prefix_sum[num] - (0 if prev_idx == -1 else prefix_sum[prev_idx]))/(num - prev_idx)
            curr_square_expectation = (square_prefix_sum[num] - (0 if prev_idx == -1 else square_prefix_sum[prev_idx]))/(num - prev_idx)
            curr_diff += curr_square_expectation - curr_expectation* curr_expectation
            prev_idx = num
        curr_expectation = (prefix_sum[length - 1] - (0 if prev_idx == -1 else prefix_sum[prev_idx]))/(length-1-prev_idx)
        curr_square_expectation = (square_prefix_sum[length - 1] - (0 if prev_idx == -1 else square_prefix_sum[prev_idx]))/(length-1-prev_idx)
        curr_diff += curr_square_expectation - curr_expectation * curr_expectation
        if curr_diff < min_diff:
            min_diff = curr_diff
            min_partition_plan = partition_plan
    print(min_diff)
    min_partition = []
    start_idx = 0
    for num in min_partition_plan:
        curr_partition = []
        for j in range(start_idx, num + 1):
            curr_partition.append([years[j], value_sum[j]])
        min_partition.append(curr_partition)
        start_idx = num + 1
    curr_partition = []
    for j in range(start_idx, length):
        curr_partition.append([years[j], value_sum[j]])
    min_partition.append(curr_partition)
    return min_partition


def partition_fitting(partition, deg):
    x_list = []
    y_list = []
    for p in partition:
        x_list.append([p[i][0] for i in range(0, len(p))])
        y_list.append([p[i][1] for i in range(0, len(p))])
    ##print(x_list)
    ##print(y_list)
    fitting_y_list = []
    for i in range(0, len(x_list)):
        args = np.polyfit(x_list[i], y_list[i], deg=deg)
        p = np.poly1d(args)
        fitting_y_list.append([p(x_list[i][j]) for j in range(0, len(x_list[i]))])
    ##print(fitting_y_list)
    return x_list, y_list, fitting_y_list


def save_plot(data_name, x, y, fit_y):
    for i in range(0, len(x)):
        plt.plot(x[i], y[i])
        plt.plot(x[i], fit_y[i])
    file_name = data_name +"_sum_fitting.jpeg"
    plt.savefig(file_name)
    return file_name



data = pd.read_excel(os.path.join("D:\dblab3\prophet-backend\data\datasets", "三个样本.xlsx"), sheet_name="样本3", header=0,skiprows=0)
data = data_preprocess.preprocess(data)
data.columns = ['ds', 'y']
data_1 = []
length = len(data['ds'].values)
for i in range(0, length):
    l = []
    l.append(data['ds'].values[i])
    l.append(data['y'].values[i])
    data_1.append(l)

for i in range(1, len(data_1)):
    data_1[i][1] += data_1[i-1][1]

res = get_partition(data_1, 4)
x, y, fit_y = partition_fitting(res, 3)
for i in range(0, len(x)):
    plt.plot(x[i], y[i])
    plt.plot(x[i], fit_y[i])
plt.show()




