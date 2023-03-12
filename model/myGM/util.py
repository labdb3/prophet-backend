import model.myGM.GM_implementation as GM_implementation
import data.data_imputation as data_imputation
import model.myGM.curve_partition as curve_partition
import numpy as np
import copy
import model.sum.sum_partition as sum_partition
import pandas as pd


def predict(origin_data, nums, peak_rate, years, cut_idx = []):
    '''
    @description: 根据所选参数利用灰度模型对产量进行预测
    :param origin_data:
    :param nums:
    :param peak_rate:
    :param years:
    :param cut_idx:
    :return:
    '''
    origin_data, cur_fit_input, origin_model_input, message = get_model_input_auto(origin_data, nums, peak_rate)
    if not message:
        return[],[],False
    k = len(origin_data)
    Nm_res, Tm_res, b_res = get_fit_res(origin_model_input)
    start = int(origin_data[0][0])
    res = []
    actual_last_year = int(origin_data[k-1][0])
    pred_last_year = int(origin_data[k-1][0]) + years
    for i in range(0, len(cur_fit_input)):
        T_pred = Tm_res[i]
        b_pred = b_res[i]
        N_pred = Nm_res[i]
        interval_start = int(cur_fit_input[i][0][0])
        k = len(cur_fit_input[i])
        interval_end = int(cur_fit_input[i][k-1][0])
        for j in range(interval_start, interval_end+1):
            temp = []
            temp.append(j)
            fit_res = 2*N_pred/(1+np.cosh(b_pred*(origin_data[j-start][0] - T_pred)))
            temp.append(fit_res)
            res.append(temp)

    while True:
        last_Tm = Tm_res[len(Tm_res) - 1]
        last_Nm = Nm_res[len(Nm_res) - 1]
        last_b = b_res[len(b_res) - 1]
        last =(int)(actual_last_year + (last_Tm - actual_last_year) *2)
        for i in range(actual_last_year + 1, min(last + 1, pred_last_year + 1)):
            temp = []
            temp.append(i)
            fit_res = 2*last_Nm/(1+np.cosh(last_b*(i - last_Tm)))
            temp.append(fit_res)
            res.append(temp)
        if last >= pred_last_year:
            break
        else:
            actual_last_year = last + 1
            origin_model_input = origin_model_input[1:, :]
            new_model_input = np.array([last_Nm, last_Tm, last_b])
            origin_model_input = np.row_stack((origin_model_input,new_model_input))
            Nm_res, Tm_res, b_res = get_fit_res(origin_model_input)
    return origin_data, res, True


def get_fit_params(origin_data, nums, peak_rate):
    origin_data, cur_fit_input, origin_input, message = get_model_input_auto(origin_data, nums, peak_rate)
    if not message:
        return [], [], [], [], False
    Tm = origin_input[:, 1].tolist()
    Nm = origin_input[:, 0].tolist()
    b = origin_input[:, 2].tolist()
    res = []
    start =int(origin_data[0][0])
    for i in range(0, len(cur_fit_input)):
        T_pred = Tm[i]
        b_pred = b[i]
        N_pred = Nm[i]
        interval_start = int(cur_fit_input[i][0][0])
        k = len(cur_fit_input[i])
        interval_end = int(cur_fit_input[i][k-1][0])
        for j in range(interval_start, interval_end+1):
            temp = []
            temp.append(j)
            fit_res = 2*N_pred/(1+np.cosh(b_pred*(origin_data[j-start][0] - T_pred)))
            temp.append(fit_res)
            res.append(temp)
    return Tm, Nm, b, res, True


def get_manual_predicting(origin_data, Tm, Nm, b, params, N_w = None, b_w = None):
    origin_data, cur_fit_input, origin_input, message = get_model_input_auto(origin_data, params['nums'], params['peak_rate'])
    if not message:
        return [], [], [], [], False
    k = len(origin_data)
    p = len(Tm)
    if p <= 1:
        return [], [], False
    if N_w is None:
        N_w = [1 for i in range(0, p)]
    if b_w is None:
        b_w = [1 for i in range(0, p)]
    sum = 0
    end_year = int(origin_data[k-1][0])
    for i in range(0, p-1):
        sum += Tm[i+1] - Tm[i]
    sum = int(sum/(p-1))
    start = int(origin_data[0][0])
    predict_Tm = Tm[p - 1] + sum
    years =(int) (predict_Tm - end_year - 1) * 2 + 1
    sum_Nm = 0
    sum_Nm_p = 0
    sum_b = 0
    sum_b_p = 0
    for i in range(0, len(Nm)):
        sum_Nm += Nm[i] * N_w[i]
        sum_Nm_p += N_w[i]
        sum_b += b[i] *b_w[i]
        sum_b_p += b_w[i]
    predict_Nm = sum_Nm/sum_Nm_p
    predict_b = sum_b/sum_b_p
    res = []
    for i in range(0, len(cur_fit_input)):
        T_pred = Tm[i]##origin_model_input[i][1]######
        b_pred = b[i]
        N_pred = Nm[i]
        interval_start = int(cur_fit_input[i][0][0])
        k = len(cur_fit_input[i])
        interval_end = int(cur_fit_input[i][k-1][0])
        for j in range(interval_start, interval_end+1):
            temp = []
            temp.append(j)
            fit_res = 2*N_pred/(1+np.cosh(b_pred*(origin_data[j-start][0] - T_pred)))
            temp.append(fit_res)
            res.append(temp)
    for i in range(1, years + 1):
        year = end_year + i
        production = 2* predict_Nm /(1 + np.cosh(predict_b*(i + end_year - predict_Tm)))
        res.append([year, production])
    return origin_data, res


def fit(origin_data, nums, peak_rate, cut_idx = []):
    origin_data, cur_fit_input, origin_input, message = get_model_input_auto(origin_data, nums, peak_rate)
    if not message:
        return [], [], [], [], [], False
    Nm_res, Tm_res, b_res = get_fit_res(origin_input)
    length = len(Nm_res)
    res = []
    cut_dict = []
    start =int(origin_data[0][0])
    for i in range(0, len(cur_fit_input)):
        T_pred = Tm_res[i]
        b_pred = b_res[i]
        N_pred = Nm_res[i]
        interval_start = int(cur_fit_input[i][0][0])
        k = len(cur_fit_input[i])
        interval_end = int(cur_fit_input[i][k-1][0])
        if i%2 == 0:
            curr_dict = dict(gt=interval_start-start-1, lte=interval_end-start, color ='blue')
        else:
            curr_dict = dict(gt=interval_start - start - 1, lte=interval_end - start, color='red')
        cut_dict.append(curr_dict)
        for j in range(interval_start, interval_end+1):
            temp = []
            temp.append(j)
            fit_res = 2*N_pred/(1+np.cosh(b_pred*(origin_data[j-start][0] - T_pred)))
            temp.append(fit_res)
            res.append(temp)
    return origin_data, res, Nm_res[:length-1].tolist(), Tm_res[:length-1].tolist(), b_res[:length-1].tolist(), cut_dict, True


def get_fit_res(origin_input):
    Tm_one = GM_implementation.first_order_GM(origin_input[:, 1])
    bm_one = GM_implementation.first_order_GM(origin_input[:, 2])
    Nm_one = GM_implementation.first_order_GM(origin_input[:, 0])
    return Nm_one, Tm_one, bm_one


def get_origin_data(data):
    data = data_imputation.preprocess(data)
    data_after_preprocess = []
    for i in range(0, len(data['y'].values)):
        l = []
        l.append(data['ds'].values[i])
        l.append(data['y'].values[i])
        data_after_preprocess.append(l)
    return data_after_preprocess

'''
  @:description: 在给定参数的支持下自动给出产量的旋回划分
  @：params
'''
def get_model_input_auto(data, nums, peak_rate):
    data = data_imputation.preprocess(data)
    data_after_preprocess = []
    for i in range(0, len(data['y'].values)):
        l = []
        l.append(data['ds'].values[i])
        l.append(data['y'].values[i])
        data_after_preprocess.append(l)
    idx =curve_partition.get_max_index(data_after_preprocess, nums, peak_rate)
    res = curve_partition.get_curve_fit_input(data_after_preprocess, idx)

    '''
    你也可以用最小误差直方图的算法划分周期旋回 代码如下
    sum = sum_partition.get_sum(data)
    min_partition = sum_partition.get_partition(sum, 5)
    res = sum_partition.get_GM_input(min_partition)
    '''

    if len(res) < 2:
        return [],[],[],False
    par = GM_implementation.cur_fit(res)
    par = np.array(par)
    cp = copy.deepcopy(par)
    return data_after_preprocess, res, cp, True


def get_gm_model_inputs_manually(data, cut_idx):
    data = data_imputation.preprocess(data)
    data_after_preprocess = []
    for i in range(0, len(data['y'].values)):
        l = []
        l.append(data['ds'].values[i])
        l.append(data['y'].values[i])
        data_after_preprocess.append(l)
    cur_fit_input = []
    pointer = 0
    for i in range(0, len(cut_idx)):
        start_year = cut_idx[i][0]
        end_year = cut_idx[i][1]
        cycle = []
        for j in range(start_year, end_year + 1):
            cycle.append(data_after_preprocess[pointer])
            pointer += 1
        cur_fit_input.append(cycle)
    if len(cur_fit_input) < 2:
        return [], [], [], False
    cur_fit_res = GM_implementation.cur_fit(cur_fit_input)
    model_input = np.array(cur_fit_res)

    return data_after_preprocess, cur_fit_input, model_input, True


def parse(input):
    res = []
    for i in range(0, len(input)):
        for j in range(0, len(input[i])):
            res.append(input[i][j])
    return res


