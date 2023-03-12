def get_max_index(data, nums, peak_rate):
    '''
    :param data: 一个二维列表，第一维度为时间序列索引，第二维度0表示年份，1表示产量
    :param nums: 寻找峰点的一个参数
    :param peak_rate: 寻找峰点的一个参数
    :return:
       一个列表，列表的元素为每个峰点的下标，升序排列
    '''
    res = []
    i = 0
    while data[i+1][1] < data[i][1] and i < len(data) + 1:
        i += 1
    if i > 0:
        res.append(i)
    while i < len(data):
        flag, idx = is_peak(data, i, peak_rate, nums)
        if not flag:
            i += 1
        else:
            res.append(idx)
            i = idx + 1
    length = len(res)
    if length == 0 or res[length - 1] < len(data) - 1:
        res.append(len(data) - 1)
    return res


def is_peak(data, index, peak_rate, nums,back_trend_rate = 0.15):
    '''
    :param data: 一个二维列表，第一维度为时间序列索引，第二维度0表示年份，1表示产量
    :param index: 时间序列索引，代表寻找峰点的开始位置
    :param peak_rate: 峰点相对于左右相邻点的增长率
    :param nums: 峰点左右点的数目 取左边与右边点数目的较小值
    :param back_trend_rate: 峰点相对于左右相邻点的最低增长率
    :return:
           一个布尔值，True表示是峰点，False反之
           一个索引，代表找到的一个峰点的下标。下一次调用寻找峰点从该索引+1开始
    '''
    peak_num = data[index][1]
    for i in range(1, nums + 1):
        if index - i <= 0 or index + i >= len(data):
            return False, - 1
        if data[index - i][1] >= data[index - i + 1][1] or data[index + i][1] >= data[index + i - 1][1]:
            return False, - 1
    before = data[index - 1][1]
    after = data[index + 1][1]
    small_peak_rate = 0.0
    small = min((peak_num - before)/ peak_num, (peak_num - after)/ peak_num)
    big = max((peak_num - before)/ peak_num, (peak_num - after)/ peak_num)
    if big < peak_rate or small < small_peak_rate:
        return False, -1
    for i in range(index + nums + 1, len(data)):
        if data[i][1] >= data[i - 1][1] and (data[i][1] - data[i-1][1]/data[i-1][1] >= back_trend_rate):
            return True, i - 1
    return True, len(data) - 1


def get_curve_fit_input(data, end_idx):
    '''
    :description: 得到python cur_fit的一个输入划分 因为我们需要分段拟合 需要给出每一段
    :param data: 数据
    :param end_idx: 每段终止位置下标的列表
    :return: 一个三维列表 第一维度的每个元素即为一个划分（一段年份产量序列）
    '''
    res = []
    start_index = 0
    for e in end_idx:
        end = []
        for j in range(start_index, e+1):
            end.append(data[j])
        if len(end) >0:
            res.append(end)
        start_index = e + 1
    return res

