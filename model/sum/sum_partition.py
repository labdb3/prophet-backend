import numpy as np
import copy
import matplotlib.pyplot as plt
import warnings



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


def check(partition, threshold = 3):
    prev_idx = -1
    for idx in partition:
        if idx - prev_idx < threshold:
            return False
        prev_idx = idx
    return True


def get_partition(input_sum, partition_num):
    '''

    :param input_sum: 一个累积曲线列表，每个元素是[年份，累积产量]
           partition_num: 划分段数
    :return:
    min_partition 一个三维列表，代表运用最小误差直方图对累积曲线进行划分的结果
    '''
    global res_list
    res_list = []
    global cur_list
    cur_list = []
    length = len(input_sum)
    ##print(length)
    '''
       D(X) = E(X^2) - E(X)^2
       这里同样对累积曲线求了前缀和，可以方便快速我们求平均值
    '''
    years = [input_sum[i][0] for i in range(0, length)]
    value_sum = [input_sum[i][1] for i in range(0, length)]
    prefix_sum = np.zeros(length)
    prefix_sum[0] = value_sum[0]
    square_prefix_sum = np.zeros(length)
    square_prefix_sum[0] = value_sum[0] * value_sum[0]
    for i in range(1, length):
        prefix_sum[i] = prefix_sum[i-1] + value_sum[i]
        square_prefix_sum[i] = square_prefix_sum[i-1] + value_sum[i]* value_sum[i]

    '''
       先使用DFS 得到对特定列表的所有划分 比如我们有一个长度为6的列表，这里以0开始的下标指代元素，那么我们可以得到partition_num为3的划分如下:
       长度为6的列表，元素之前有5个空隙，那么我们得到个数为3的划分 等价于从5个空隙中选择两个 这个选择方案可以通过dfs给出
    '''
    res_list = dfs(cur_idx=0, cur_length=0, n=length - 1, m=partition_num)
    min_diff = 1e11
    '''
       找到方差之和最小的选择方案
    '''
    min_partition_plan = []
    for partition_plan in res_list:
        if not check(partition_plan):
            continue
        curr_diff = 0e0
        prev_idx = -1
        for num in partition_plan:
            ##print(str(num) + " "+ str(prev_idx))
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
    '''
    print("----")
    print(min_partition)
    print("----")
    '''
    return min_partition


def get_GM_input(min_partition):
    GM_input = []
    prev = 0
    for i in range(0, len(min_partition)):
        curr = []
        for j in range(0, len(min_partition[i])):
            curr.append([min_partition[i][j][0], min_partition[i][j][1] - prev])
            prev = min_partition[i][j][1]
        GM_input.append(curr)
    return GM_input


def partition_fitting(partition, deg):
    '''
    @:description: 根据分段结果对原曲线进行多项式拟合
    :param partition: 划分方案
    :param deg: 对原曲线进行分段多项式拟合的最大多项式次数
    :return:
    x_list:原始年份列表
    y_list:原始产量列表
    fitting_y_list:拟合产量列表
    args_list: 多项式参数列表
    '''
    max_deg = 4
    x_list = []
    y_list = []
    for p in partition:
        x_list.append([p[i][0] for i in range(0, len(p))])
        y_list.append([p[i][1] for i in range(0, len(p))])
    fitting_y_list = []
    args_list = []
    for i in range(0, len(x_list)):
        deg = 1
        for deg in range(1, max_deg + 1):
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                try:
                    args = np.polyfit(x_list[i], y_list[i], deg=deg)
                except np.RankWarning:
                    break
        deg -= 1
        print(deg)
        args = np.polyfit(x_list[i], y_list[i], deg=deg)
        args_list.append(args)
        p = np.poly1d(args)
        fitting_y_list.append([p(x_list[i][j]) for j in range(0, len(x_list[i]))])
    print(x_list)
    print(y_list)
    print(fitting_y_list)
    print(fitting_y_list[0])
    return x_list, y_list, fitting_y_list, args_list


def save_plot(data_name, x, y, fit_y):
    plt.figure()
    for i in range(0, len(x)):
        plt.plot(x[i], y[i], ls='-', color='r', label='actual')
        plt.plot(x[i], fit_y[i], ls='--', color ='b',label='fitting')
        plt.legend(['actual_sum', 'fitting_sum'])
    sum_file_name = "static/demo_sum.jpeg"
    plt.savefig(sum_file_name)
    plt.figure()
    sum_y = []
    sum_fit_y = []
    sum_x = []
    actual_y = []
    actual_fit_y = []
    for i in range(0, len(x)):
        for j in range(0, len(x[i])):
            sum_x.append(x[i][j])
            sum_y.append(y[i][j])
            sum_fit_y.append(fit_y[i][j])
    actual_y.append(sum_y[0])
    actual_fit_y.append(sum_fit_y[0])
    for i in range(1, len(sum_x)):
        actual_y.append(sum_y[i] - sum_y[i-1])
        actual_fit_y.append(sum_fit_y[i] - sum_fit_y[i-1])
    plt.plot(sum_x, actual_y, ls='-', color='r', label='actual')
    plt.plot(sum_x, actual_fit_y, ls='--', color='b', label='fitting')
    plt.legend(['actual', 'fitting'])
    actual_file_name = "static/demo_actual.jpeg"
    plt.savefig(actual_file_name)
    return sum_file_name, actual_file_name


def get_poly(ploy_coefficients_list, n):
    '''
    @:description: 得到多项式字符串
    :param ploy_coefficients_list: 多项式系数列表
    :param n: 多项式最高次数
    :return: 一个多项式字符串
    '''
    if n >= 2:
        if ploy_coefficients_list[0] == 1:
            Fx = 'x^{}'.format(n)
        elif ploy_coefficients_list[0] == -1:
            Fx = '-x^{}'.format(n)
        else:
            Fx = '{}x^{}'.format(ploy_coefficients_list[0], n)
    else:
        Fx = '{}x'.format(ploy_coefficients_list[0])
    for i in range(1, n - 1):
        if ploy_coefficients_list[i] > 0 and ploy_coefficients_list[i] != 1:
            Fx = Fx + '+{}x^{}'.format(ploy_coefficients_list[i], n - i)
        elif ploy_coefficients_list[i] == 1:
            Fx = Fx + '+x^{}'.format(n - i)
        elif ploy_coefficients_list[i] < 0 and ploy_coefficients_list[i] != -1:
            Fx = Fx + '{}x^{}'.format(ploy_coefficients_list[i], n - i)
        elif ploy_coefficients_list[i] == -1:
            Fx = Fx + '-x^{}'.format(n - i)

    if n >= 2:
       if ploy_coefficients_list[-2] > 0 and ploy_coefficients_list[-2] != 1:
           Fx = Fx + '+{}x'.format(ploy_coefficients_list[-2])
       elif ploy_coefficients_list[-2] == 1:
           Fx = Fx + '+x'
       elif ploy_coefficients_list[-2] < 0 and ploy_coefficients_list[-2] != -1:
           Fx = Fx + '{}x'.format(ploy_coefficients_list[-2])
       elif ploy_coefficients_list[-2] == -1:
           Fx = Fx + '-x'

    if ploy_coefficients_list[-1] > 0:
        Fx = Fx + '+{}'.format(ploy_coefficients_list[-1])
    elif ploy_coefficients_list[-1] < 0:
        Fx = Fx + '{}'.format(ploy_coefficients_list[-1])

    return Fx


'''
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

represent = [[394, 558, 660, 471, 575, 574, 2894, 1919, 1616, 1931, 2957, 7337, 3436, 2843, 3393, 4639, 4750, 3967, 4112, 4032, 1879, 1163, 2488, 1072, 1269, 1659, 2367, 2634, 3318, 3441, 3234, 3481, 3518, 576, 175, 223, 321, 226, 226, 189, 122, 205, 203, 166, 233, 300, 233, 166],
             [950, 1225, 9180, 2103, 1800, 3063, 2757, 4335, 4803, 1492, 1383, 5168, 5099, 3570, 3738, 2117, 2529, 4078,
              5883, 5171, 9164, 16989, 8596, 8309, 4743, 4473, 4466, 4102, 3752, 3945, 4269, 5164, 5089, 4249, 6172,
              4852, 7333, 6595, 7128, 7378, 8351, 12454, 7215, 5650, 8232, 9754, 9326, 7988, 8596, 8640, 6813, 5231,
              6194, 5429, 7100, 7260, 7157, 7049, 5333, 6666, 6666, 6666, 6666],
             [157, 216, 235, 314, 640, 453, 535, 1727, 4464, 766, 880, 721, 519, 546, 381, 782, 892, 1635, 1766, 2301,
              1662, 1587, 1848, 1296, 3190, 1951, 2551, 1516, 1056, 860, 506, 532, 1291, 1200, 732, 846, 750, 666, 500,
              500, 500],
[1426, 10069, 11077, 4076, 2458, 4010, 4496, 3496, 2890, 1733, 3007, 7491, 5136, 1661, 584, 1464, 2713, 3161, 3034, 5301, 9609, 17881, 11244, 8823, 5907, 5391, 6246, 5442, 4912, 4819, 5575, 5578, 5660, 5517, 7226, 5623, 5765, 5426, 6129, 9017, 6408, 5883, 4830, 6043, 6063, 5842, 5727, 7053, 5185, 4091, 1563, 981, 621, 709, 1555, 1129, 1519, 1501, 1600, 1433, 1366, 1200, 1233]
]

for i in range(0, len(represent)):
    sum_input = []
    prev = 0
    for j in range(0, len(represent[i])):
        sum_input.append([j, represent[i][j]+prev])
        prev = represent[i][j] + prev
    sum_partition = get_partition(sum_input, 5)
    x, y, fitting_y = partition_fitting(sum_partition, 3)
    save_plot(str(i), x, y, fitting_y)
'''



