from tslearn.utils import to_time_series_dataset
from tslearn.clustering import TimeSeriesKMeans, silhouette_score
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# sheet_name 要参与聚类的文件名[sheet_name1,sheet_name2,sheet_name3,.....]
# data sheet_name对应的储量值数据

def k_means(sheet_name:list, data:list):
    X = to_time_series_dataset(data)
    # 数据标准化
    X = TimeSeriesScalerMeanVariance(mu=0.0, std=1.0).fit_transform(X)
    n_clusters = 4
    km = TimeSeriesKMeans(n_clusters=n_clusters, metric="dtw")
    labels = km.fit_predict(X)
    plt.figure(figsize=(8, 8), dpi=80)
    #plt.figure(1)
    ax1 = plt.subplot(221)
    ax2 = plt.subplot(222)
    ax3 = plt.subplot(223)
    ax4 = plt.subplot(224)

    title1 = ''
    title2 = ''
    title3 = ''
    title4 = ''
    for x in range(len(labels)):
        if labels[x] == 0:
            title1 += ' '+str(sheet_name[x])
        elif labels[x] == 1:
            title2 += ' '+str(sheet_name[x])
        elif labels[x] == 2:
            title3 += ' '+str(sheet_name[x])
        elif labels[x] == 3:
            title4 += ' '+str(sheet_name[x])

    ax1.set_title(title1, fontsize='x-small')
    ax2.set_title(title2, fontsize='x-small')
    ax3.set_title(title3, fontsize='x-small')
    ax4.set_title(title4, fontsize='x-small')

    for x in range(len(labels)):
        if labels[x] == 0:
            ax1.plot(range(len(data[x])), data[x], color="r", linestyle="--")
        elif labels[x] == 1:
            ax2.plot(range(len(data[x])), data[x], color="y", linestyle="--")
        elif labels[x] == 2:
            ax3.plot(range(len(data[x])), data[x], color="b", linestyle="--")
        elif labels[x] == 3:
            ax4.plot(range(len(data[x])), data[x], color="g", linestyle="--")

    plt.savefig("demo.jpeg")

