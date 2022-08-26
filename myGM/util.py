import myGM.xlsx_reader as xlsx_reader
import myGM.data_preprocess as data_preprocess
import numpy as np
import copy


def predict(data,years):
    data, cur_fit_input, origin_input, model_input, stat = get_model_input(data)
    Nm_res, Tm_res, b_res = get_fit_res(origin_input, model_input, stat)
    for i in range(0, len(b_res)):
        b_res[i] = b_res[i] * stat[2][1] + stat[2][0]
        Nm_res[i] = Nm_res[i] * stat[0][1] + stat[0][0]
    res = []
    cnt = 0
    for i in range(0, len(cur_fit_input)):
        T_pred = Tm_res[i]
        b_pred = b_res[i]
        N_pred = Nm_res[i]
        for j in range(0, len(cur_fit_input[i])):
            temp = []
            temp.append(data[cnt][0])
            cnt += 1
            fit_res = 2 * N_pred / (1 + np.cosh(b_pred * (data[cnt][0] - T_pred)))
            temp.appned(fit_res)
            res.append(temp)
    k = len(data)
    p = len(b_res)
    pred_b = b_res[p-1]
    pred_N = Nm_res[p-1]
    pred_Tm = Tm_res[p-1]
    start_year = data[k-1][0]
    for i in range(1, years + 1):
        temp = []
        temp.append(i+start_year)
        fit_res = 2 * pred_N / (1 + np.cosh(pred_b * (i+start_year - pred_Tm)))
        temp.append(fit_res)
        res.append(temp)
    return data, res
    '''
    k = len(data)
    p = len(origin_input[1])
    last_year = data[k-1][0] + years
    Tm_list = origin_input[1,:]
    curr_year = origin_input[1][p-1]
    cnt = 0
    while curr_year<last_year:
        cnt += 1
        fitting_Tm = xlsx_reader.first_order_GM(Tm_list)
        curr_year = fitting_Tm[len(fitting_Tm) - 1]
        Tm_list = np.append(Tm_list, curr_year)

    for i in range(0, cnt):
        j = 1
    '''


def fit(data):
    ## data: 经过处理以后的年份和产量列表
    #origin_input:未经过归一化处理
    # model_input: 灰度模型N,T,b输入,经过归一化处理
    #cur_fit_input:
    #stat: 将来用于归一化还原的统计量信息
    data, cur_fit_input, origin_input, model_input, stat = get_model_input(data)
    Nm_res, Tm_res, b_res = get_fit_res(origin_input, model_input, stat)
    for i in range(0, len(b_res)):
        b_res[i] = b_res[i] * stat[2][1] + stat[2][0]
        Nm_res[i] = Nm_res[i] * stat[0][1] + stat[0][0]
    res = []
    cnt = 0
    for i in range(0, len(cur_fit_input)):
        T_pred = Tm_res[i]
        b_pred = b_res[i]
        N_pred = Nm_res[i]
        for j in range(0, len(cur_fit_input[i])):
            temp = []
            temp.append(data[cnt][0])
            cnt += 1
            fit_res = 2*N_pred/(1+np.cosh(b_pred*(data[cnt][0] - T_pred)))
            temp.appned(fit_res)
            res.append(temp)
    return data, res


def get_fit_res(origin_input, model_input, stat):
    Nm_actual = model_input[:, 0]
    Nm_relevant = model_input[:, 1:]
    b_actual = model_input[:, 2]
    b_relevant = model_input[:, (0, 1)]
    b_res = xlsx_reader.GM_predict(b_actual, b_relevant, 'b')
    Nm_res = xlsx_reader.GM_predict(Nm_actual, Nm_relevant, 'Nm')
    Tm_res = xlsx_reader.first_order_GM(origin_input[1,:])
    for i in range(0, len(b_res)):
        b_res[i] = b_res[i] * stat[2][1] + stat[2][0]
        Nm_res[i] = Nm_res[i] * stat[0][1] + stat[0][0]
    return Nm_res, Tm_res, b_res


def get_model_input(data):
    pre = data
    data = []
    length = len(pre['y'].values)
    for i in range(0, length):
        l = []
        l.append(pre['ds'].values[i])
        l.append(pre['y'].values[i])
        data.append(l)
    idx = data_preprocess.get_max_index(data)
    res = data_preprocess.get_curve_fit_input(data, idx)
    par = xlsx_reader.cur_fit(res)
    par = np.array(par)
    model_input, stat = xlsx_reader.normalization(par)
    return data, res, par, model_input, stat

