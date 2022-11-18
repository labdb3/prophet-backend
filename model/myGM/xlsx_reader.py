from openpyxl import load_workbook
import numpy as np
import copy
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def get_lines(path):
    table = load_workbook(path)
    sheet_name = table.get_sheet_names()
    first_sheet = table.get_sheet_by_name(sheet_name[0])
    rows = first_sheet.rows
    col = first_sheet.columns

    lines = []
    for row in rows:
        line = [col.value for col in row]
        lines.append(line)

    lines = lines[1:]
    ## generate into sub_sequences
    return lines


lines = [[[1986, 77.47], [1987, 110], [1988, 211.77], [1989, 172.1]],
         [[1990, 178.02], [1991, 210.01], [1992, 235.33], [1993, 565.48], [1994, 307.66]],
         [[1995, 353.55], [1996, 501.16], [1997, 380.53], [1998, 376.59]],
         [[1999, 453.65], [2000, 609.16], [2001, 118.13]],
         [[2002, 721.98], [2003, 598.84], [2004, 1885.53], [2005, 2243.53], [2006, 2258.9], [2007, 1335.52]],
         [[2008, 1422.04], [2009, 2585.99], [2010, 1171.19]],
         [[2011, 2885.22], [2012, 3382.53], [2013, 4949.98], [2014, 163.82]],
         [[2015, 2185.94], [2016, 1632.11], [2017, 682.96]],
         [[2018, 473.36], [2019, 1955.85], [2020, 2177.56]]
         ]


def first_order_GM(actual):
    ##np.insert(actual,0, 0)
    sum_act = actual.cumsum(axis=0)
    Z = np.array(([-0.5 * (sum_act[k - 1] + sum_act[k]) for k in range(1, len(sum_act))])).reshape(len(sum_act) - 1, 1)
    one = np.ones((len(actual) - 1, 1))
    B = np.hstack((Z,one))
    Y = (actual[1:].reshape(len(Z), 1))
    u = np.linalg.inv(np.matmul(B.T, B)).dot(B.T).dot(Y)
    a = u[0][0]
    b = u[1][0]
    sum_res = np.zeros(len(actual)+1)
    for i in range(0, len(sum_res)):
        sum_res[i] = (actual[0] - b/a) *np.exp(-a*i) + b/a
    actual_res = np.zeros(len(actual)+1)
    actual_res[0] = sum_res[0]
    for i in range(1, len(actual_res)):
        actual_res[i] = sum_res[i] - sum_res[i-1]
    return actual_res


def GM_predict(actual, relevant, type= 'Nm'):
    X = relevant.cumsum(axis=0)
    sum_act = actual.cumsum(axis= 0)
    Z = np.array(([-0.5 *(sum_act[k - 1] + sum_act[k]) for k in range(1, len(sum_act))])).reshape(len(sum_act) - 1, 1)
    Y = (actual[1:].reshape(len(Z), 1))
    k = len(Z)
    B = np.hstack((Z, X[1:, :]))

    u = np.linalg.inv(np.matmul(B.T, B)).dot(B.T).dot(Y)
    b1 = u[0][0]
    b2 = u[1][0]
    b3 = u[2][0]
    sum_res = np.zeros(k+1)
    for i in range(1,k+1):
        sum_res[i] = (actual[0]-(b2*X[i][0] + b3*X[i][1])/b1)*np.exp(-b1*(i)) + (b2*X[i][0] + b3*X[i][1])/b1
    pred_res = []
    pred_res.append(actual[0])
    for i in range(0, k):
        pred = 0
        if i == 0:
            pred = sum_res[i] - pred_res[0]
        else:
            pred = sum_res[i] - pred_res[i - 1]
        if type == 'Nm':
            pred = max(pred, 0)
        pred_res.append(pred)
    return pred_res




def cur_fit(lines):
    res = []
    for line in lines:
        l = []
        arr = np.array(line)
        x = arr[:, 0]
        y = arr[:, 1]
        l.append(x)
        l.append(y)
        Nm, Tm = get_Nm_and_Tm(line)
        ##fig, ax = plt.subplots()

        def hubbert_function(x, b):
            return 2 * Nm / (1 + np.cosh(b * (x - Tm)))

        popt, pcov = curve_fit(hubbert_function, x, y, maxfev = 10000)
        y2 = [hubbert_function(xx, popt[0], ) for xx in x]
        res.append([Nm, Tm, popt[0]])

    return res


def draw(pred, actual):
    X = [k+1 for k in range(0, len(pred))]
    fig, ax = plt.subplots()
    l = actual
    ##l.append(0)
    ax.plot(X, pred, 'b-', label='predicting values')
    ax.plot(X, l, 'r--', label='actual value')
    ##plt.ylim(1900,2100)
    ax.legend(['predicting', 'actual'])
    plt.show()


def get_Nm_and_Tm(line):
    Tm = line[0][0]
    Nm = line[0][1]
    for l in line:
        if l[1] > Nm:
            Tm = l[0]
            Nm = l[1]
    return Nm, Tm


def normalization(origin_list):
    parms = []
    for j in range(0, 3):
        l = []
        sum = 0
        var = 0
        for i in range(0, len(origin_list)):
            sum += origin_list[i][j]
        mean = sum/len(origin_list)
        l.append(mean)
        for i in range(0, len(origin_list)):
            var += (mean - origin_list[i][j]) * (mean - origin_list[i][j])
        var /= len(origin_list)
        var = np.sqrt(var)
        l.append(var)
        for i in range(0, len(origin_list)):
            origin_list[i][j] = (origin_list[i][j] - mean)/var
        parms.append(l)
    return origin_list, parms
'''
N_ms = [27087, 9196, 7569, 4451, 16476, 4656, 4858]
T_ms = [1965, 1970, 1975, 1981, 1984, 1989, 1994]
b_s = [3.0592149250599454, 3.3965766305346263, 1.7741362407262584, 1.7527531907723224, 1.371244308737967, 0.21909357713544134,0.8751651491068586]
##N_ms, T_ms, b_s = cur_fit(lines)
res = cur_fit(lines)
par = np.array(res)
temp = copy.deepcopy(par)
par, stat = normalization(par)
Nm_actual = par[:, 0]
Nm_relevant = par[:, 1:]
Tm_actual = par[:, 1]
Tm_relevant = par[:, (0, 2)]
b_actual = par[:, 2]
b_relevant = par[:, (0, 1)]
res = GM_predict(b_actual, b_relevant)
for i in range(0, len(res)):
    res[i] = res[i]*stat[2][1] + stat[2][0]
    '''

##draw(res, temp[:, 2])
##N_mean, N_var, N_l = normalization(N_ms)
##T_mean, T_var , T_l = normalization(T_ms)
##b_mean, b_var, b_l = normalization(b_s)
##nor_T = GM_predict(N_l, b_l)
##nor_N = GM_predict(T_l, b_l)
##nor_b = GM_predict(N_l, T_l)
##new_T = nor_T*T_var + T_mean
##new_b = nor_b*b_var + b_mean
##new_N = nor_N*N_var + N_mean

##print(new_T)
##print(new_b)
##print(new_N)
##print(2 * new_N / (1 + np.cosh(new_b * (2021 - new_T))))
