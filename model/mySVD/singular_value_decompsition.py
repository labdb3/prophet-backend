'''数据处理'''
import pandas as pd
import numpy as np
from data.preprocess import BASE_DIR
'''数据可视化'''
import matplotlib.pyplot as plt
import os
'''
plt.rcParams['figure.dpi'] = 800  # 调整分辨率
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
'''



# 算法封装
class SSA(object):
    __supported_types = (pd.Series, np.ndarray, list)  # 限制时间序列的输入类型

    def __init__(self, tseries, L):
        '''
        Args:
            tseries:原始时间序列
            L:窗口长度
        '''

        if not isinstance(tseries, self.__supported_types):
            raise TypeError("请确保时间序列的数据类型为Pandas Series,NumpPy array 或者list")
        else:
            self.orig_TS = pd.Series(tseries)

        self.N = len(tseries)  # 原始时间序列长度
        if not 2 <= L <= self.N / 2:
            raise ValueError("窗口长度必须介于[2,N/2]")
        self.L = L  # 窗口长度，轨迹矩阵的行数
        self.K = self.N - self.L + 1  # 轨迹矩阵的列数
        self.X = np.array([self.orig_TS.values[i:L + i] for i in range(0, self.K)]).T

        # 奇异值分解
        self.U, self.Sigma, VH = np.linalg.svd(self.X)
        self.r = np.linalg.matrix_rank(self.X)  # 矩阵的秩等于非零特征值的数量
        # 每一个非零特征值都对应一个子矩阵，子矩阵对角平均化后得到原始时间序列的一个子序列
        self.TS_comps = np.zeros((self.N, self.r))

        # 对角平均还原
        for i in range(self.r):
            X_elem = self.Sigma[i] * np.outer(self.U[:, i], VH[i, :])
            X_rev = X_elem[::-1]
            self.TS_comps[:, i] = [X_rev.diagonal(j).mean() for j in range(-X_rev.shape[0] + 1, X_rev.shape[1])]

    def comps_to_df(self):
        '''将子序列数组转换成DataFrame类型
        '''
        cols = ["F{}".format(i) for i in range(self.r)]
        return pd.DataFrame(data=self.TS_comps, columns=cols, index=self.orig_TS.index)

    def reconsruct(self, indices):
        '''重构，可以是部分重构（相当于子序列的分组合并），也可以是全部合并（重构为原序列）
        Args:
            indices   重构所选择的子序列
        '''
        if isinstance(indices, int):
            indices = [indices]

        ts_vals = self.TS_comps[:, indices].sum(axis=1)
        print(len(ts_vals))
        return pd.Series(ts_vals, index=self.orig_TS.index)

    def vis(self):
        '''可视化子序列
        '''
        fig, axs = plt.subplots(self.r, sharex='all')
        for i in range(self.r):
            axs[i].plot(self.reconsruct(i),'r', lw=1)
            axs[i].plot(self.orig_TS, 'b')
        plt.show()


###加载数据集###
file = r'D:/机器学习/crude-oil-price.csv'
oil_info = pd.read_excel(os.path.join(BASE_DIR, '三个样本.xlsx'), header = 0,  sheet_name='样本1', skiprows=0)
oil_info.columns = ['ds', 'y']
price = oil_info['y']
price_SSA = SSA(price, 3)
comps_df = price_SSA.comps_to_df()
price_SSA.vis()
