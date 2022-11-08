import model.myGM.xlsx_reader as xlsx_reader
import model.myGM.data_preprocess as data_preprocess
import numpy as np
import copy
import pandas as pd


def get_preprocess(data):
    return 0


def predict(origin_data, nums, peak_rate, years, cut_idx = []):
    origin_data, cur_fit_input, origin_model_input, message = get_model_input(origin_data, nums, peak_rate)
    if not message:
        return[],[],False
    k = len(origin_data)
    Nm_res, Tm_res, b_res = get_fit_res(origin_model_input)
    start = int(origin_data[0][0])
    res = []
    actual_last_year = int(origin_data[k-1][0])
    pred_last_year = int(origin_data[k-1][0]) + years
    for i in range(0, len(cur_fit_input)):
        T_pred = Tm_res[i]##origin_model_input[i][1]######
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


def pred(origin_data, nums, peak_rate, years, cut_idx = []):
    origin_data, cur_fit_input, origin_model_input, message = get_model_input(origin_data, nums, peak_rate)
    if not message:
        return [],[], False
    Nm_res, Tm_res, b_res = get_fit_res(origin_model_input)

    '''
    for i in range(0, len(b_res)):
        b_res[i] = b_res[i] * stat[2][1] + stat[2][0]
        Nm_res[i] = Nm_res[i] * stat[0][1] + stat[0][0]
    '''
    res = []
    start = int(origin_data[0][0])
    for i in range(0, len(cur_fit_input)):
        T_pred = Tm_res[i]##origin_model_input[i][1]######
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
    p = len(b_res)
    pred_b = b_res[p-1]
    pred_N = Nm_res[p-1]
    pred_Tm = Tm_res[p-1]

    start_year = origin_data[len(origin_data)-1][0]
    for i in range(1, years + 1):
        temp = []
        temp.append(i+start_year)
        fit_res = 2 * pred_N / (1 + np.cosh(pred_b * (i+start_year - pred_Tm)))
        temp.append(fit_res)
        res.append(temp)
    return origin_data, res, True
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


def fit(origin_data, nums, peak_rate, cut_idx = []):
    ## data: 经过处理以后的年份和产量列表
    #origin_input:未经过归一化处理
    # model_input: 灰度模型N,T,b输入,经过归一化处理
    #cur_fit_input:
    #stat: 将来用于归一化还原的统计量信息
    origin_data, cur_fit_input, origin_input, message = get_model_input(origin_data, nums, peak_rate)
    if not message:
        return [],[], False
    Nm_res, Tm_res, b_res = get_fit_res(origin_input)
    '''
    for i in range(0, len(b_res)):
        b_res[i] = b_res[i] * stat[2][1] + stat[2][0]
        Nm_res[i] = Nm_res[i] * stat[0][1] + stat[0][0]
    '''
    res = []
    start = origin_data[0][0]
    for i in range(0, len(cur_fit_input)):
        T_pred = Tm_res[i]
        b_pred = b_res[i]
        N_pred = Nm_res[i]
        interval_start = cur_fit_input[i][0][0]
        k = len(cur_fit_input[i])
        interval_end = cur_fit_input[i][k-1][0]
        for j in range(interval_start, interval_end+1):
            temp = []
            temp.append(j)
            fit_res = 2*N_pred/(1+np.cosh(b_pred*(origin_data[j-start][0] - T_pred)))
            temp.append(fit_res)
            res.append(temp)
    return origin_data, res,True


def get_fit_res(origin_input):
    Tm_one = xlsx_reader.first_order_GM(origin_input[:, 1])
    bm_one = xlsx_reader.first_order_GM(origin_input[:, 2])
    Nm_one = xlsx_reader.first_order_GM(origin_input[:, 0])
    '''
    k = len(Tm_one)
    print([Nm_one[k-1],Tm_one[k-1],bm_one[k-1]])
    Tm = (Tm_one[k-1]-stat[1][0])/stat[1][1]
    Nm = (Nm_one[k-1] -stat[0][0])/stat[0][1]
    bm = (bm_one[k-1] - stat[2][0])/stat[2][1]
    arr = [Nm,Tm,bm]
    model_input = np.row_stack((model_input,np.array(arr)))
    Nm_actual = model_input[:, 0]
    Nm_relevant = model_input[:, 1:]
    b_actual = model_input[:, 2]
    b_relevant = model_input[:, (0, 1)]
    b_res = xlsx_reader.GM_predict(b_actual, b_relevant, 'b')
    Nm_res = xlsx_reader.GM_predict(Nm_actual, Nm_relevant, 'Nm')
    '''
    return Nm_one, Tm_one, bm_one


def get_model_input(data, nums, peak_rate):
    data = data_preprocess.preprocess(data)
    data_after_preprocess = []
    for i in range(0, len(data['y'].values)):
        l = []
        l.append(data['ds'].values[i])
        l.append(data['y'].values[i])
        data_after_preprocess.append(l)
    idx = data_preprocess.get_max_index(data_after_preprocess, nums, peak_rate)
    res = data_preprocess.get_curve_fit_input(data_after_preprocess, idx)
    if len(res) < 2:
        return [],[],[],False
    par = xlsx_reader.cur_fit(res)
    par = np.array(par)
    cp = copy.deepcopy(par)
    return data_after_preprocess, res, cp, True


def get_m_input(data, cut_idx):
    data = data_preprocess.preprocess(data)
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
    cur_fit_res = xlsx_reader.cur_fit(cur_fit_input)
    model_input = np.array(cur_fit_res)

    return data_after_preprocess, cur_fit_input, model_input, True


def parse(input):
    res = []
    for i in range(0, len(input)):
        for j in range(0, len(input[i])):
            res.append(input[i][j])
    return res

'''
data = [[1963, 865.5010998412718], [1964, 6103.340758376175], [1965, 21794.28733381539], [1966, 7632.706643012204], [1967, 5692.798998798731], [1968, 8210.687963866745], [1969, 7591.465924272708], [1970, 8793.773745011611], [1971, 10566.40827273803], [1972, 3403.220152530498], [1973, 4481.532801516159], [1974, 13596.67257339513], [1975, 14240.765131607], [1976, 11172.04879800278], [1977, 9660.157652777536], [1978, 4768.712750752036], [1979, 5604.647473049868], [1980, 7972.751557898135], [1981, 11983.32416853319], [1982, 12574.71522727473], [1983, 26021.86437866144], [1984, 42336.12775881473], [1985, 28367.82390731853], [1986, 23291.79912647539], [1987, 14822.70602222533], [1988, 13250.93114834253], [1989, 13108.92845776015], [1990, 12123.74329428499], [1991, 11201.46856312764], [1992, 11378.09307342848], [1993, 12672.33574582579], [1994, 15119.97810638444], [1995, 14570.17246123067], [1996, 13729.21362044544], [1997, 17062.27678202768], [1998, 16040.54655653387], [1999, 20856.28608718407], [2000, 20267.93447463253], [2001, 21196.91571070117], [2002, 21962.38110332668], [2003, 27041.17103750576], [2004, 34532.07181042249], [2005, 22260.75143043707], [2006, 18079.76103848408], [2007, 24332.90084296809], [2008, 28947.91397272871], [2009, 27637.03964603366], [2010, 24584.91227940025], [2011, 25840.50752081556], [2012, 25490.91697159208], [2013, 20198.72037770855], [2014, 16550.47936653839], [2015, 17691.04849304369], [2016, 17128.68276316575], [2017, 20838.78182074191], [2018, 21783.19168957896], [2019, 21773.28594027495], [2020, 20336.71754915257], [2021, 16987.26949691674], [2022, 19513.67765296784], [2023, 20035.67868087464], [2024, 20023.62268086542], [2025, 20000.88263951719]]
cur_fit_input = [[[1963, 865.5010998412718], [1964, 6103.340758376175], [1965, 21794.28733381539], [1966, 7632.706643012204]],
                 [[1967, 5692.798998798731], [1968, 8210.687963866745], [1970, 8793.773745011611], [1971, 10566.40827273803],[1972, 3403.220152530498]],
      [ [1973, 4481.532801516159], [1974, 13596.67257339513], [1975, 14240.765131607], [1976, 11172.04879800278], [1977, 9660.157652777536], [1978, 4768.712750752036]],
      [[1979, 5604.647473049868], [1980, 7972.751557898135], [1981, 11983.32416853319], [1982, 12574.71522727473], [1983, 26021.86437866144], [1984, 42336.12775881473], [1985, 28367.82390731853], [1986, 23291.79912647539], [1987, 14822.70602222533], [1988, 13250.93114834253], [1989, 13108.92845776015], [1990, 12123.74329428499], [1991, 11201.46856312764]],
      [[1992, 11378.09307342848], [1993, 12672.33574582579], [1994, 15119.97810638444], [1995, 14570.17246123067]],
      [[1996, 13729.21362044544], [1997, 17062.27678202768], [1998, 16040.54655653387], [1999, 20856.28608718407], [2000, 20267.93447463253], [2001, 21196.91571070117], [2002, 21962.38110332668], [2003, 27041.17103750576], [2004, 34532.07181042249], [2005, 22260.75143043707]],
      [[2006, 18079.76103848408], [2007, 24332.90084296809], [2008, 28947.91397272871], [2009, 27637.03964603366], [2010, 24584.91227940025], [2013, 20198.72037770855], [2014, 16550.47936653839]],
      [[2015, 17691.04849304369], [2016, 17128.68276316575], [2017, 20838.78182074191], [2018, 21783.19168957896],[2019, 21773.28594027495], [2020, 20336.71754915257], [2021, 16987.26949691674]],
      [[2022, 19513.67765296784], [2023, 20035.67868087464], [2024, 20023.62268086542], [2025, 20000.88263951719]]
      ]
origin, res = fit(data, cur_fit_input)
print(origin)
print(res)
xlsx_reader.draw(res, data)
'''
'''
data = pd.read_excel("D:\dblab3\prophet-backend\data\datasets\三个样本.xlsx", skiprows=0,sheet_name="样本1")
origin,res = fit(data, 1, 0.3)
xlsx_reader.draw(res, origin)
'''

