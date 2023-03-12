import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def first_order_GM(actual):
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
    '''
    @:description:
    :param actual:
    :param relevant:
    :param type:
    :return:
    '''
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

        def hubbert_function(x, b):
            return 2 * Nm / (1 + np.cosh(b * (x - Tm)))

        popt, pcov = curve_fit(hubbert_function, x, y, maxfev = 10000)
        res.append([Nm, Tm, popt[0]])

    return res


def draw_actual(actual):
    years = [x[0] for x in actual]
    production = [x[1] for x in actual]
    fig, ax = plt.subplots()
    ax.plot(years, production,'b-')
    ax.legend(['actual'])
    plt.show()


def draw_pred(pred):
    years = [x[0] for x in pred]
    production = [x[1] for x in pred]
    fig, ax = plt.subplots()
    ax.plot(years, production,'b-')
    ax.legend(['pred'])
    plt.show()


def draw(pred, actual):
    X = [k+1 for k in range(0, len(pred))]
    fig, ax = plt.subplots()
    l = actual
    ax.plot(X, pred, 'b-', label='predicting values')
    ax.plot(X, l, 'r--', label='actual value')
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
    '''
    @description: 在多维灰度模型中 我们需要对各个参数进行归一化 归一化为均值方差相同的数据
    但是根据实验结果多维的效果显然不如一维 所以我们没有采用
    :param origin_list:
    :return:
    '''
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
