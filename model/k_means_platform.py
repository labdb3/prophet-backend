import matplotlib
from tslearn.utils import to_time_series_dataset
from tslearn.clustering import TimeSeriesKMeans, silhouette_score
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
import matplotlib.pyplot as plt

# sheet_name 要参与聚类的文件名[sheet_name1,sheet_name2,sheet_name3,.....]
# data sheet_name对应的储量值数据

'''
   解决中文乱码问题
'''
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

##plt.rcParams['font.sans-serif']= ['Songti SC']
matplotlib.use('Agg')
##font_list = sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])



def k_means(sheet_name:list, data:list):
    """
     @:description k_means聚类算法，用于对产量曲线进行聚类

    """

    X = to_time_series_dataset(data)
    # 数据标准化
    X = TimeSeriesScalerMeanVariance(mu=0.0, std=1.0).fit_transform(X)
    n_clusters = 4
    scores = 1
    labels = []
    for i in range(20):
        km = TimeSeriesKMeans(n_clusters=n_clusters, n_init=10, max_iter=3000, metric="dtw",random_state=i)
        label = km.fit_predict(X)
        score = silhouette_score(X, label, metric="dtw")
        if score < scores:
            scores = score
            labels = label

    # 获取代表曲线
    label1 = []
    label2 = []
    label3 = []
    label4 = []

    for i in range(len(labels)):
        if labels[i] == 0:
            label1.append(i)
        elif labels[i] == 1:
            label2.append(i)
        elif labels[i] == 2:
            label3.append(i)
        else:
            label4.append(i)

    max_len1 = 0
    max_len2 = 0
    max_len3 = 0
    max_len4 = 0
    for i in label1:
        if len(data[i]) > max_len1:
            max_len1 = len(data[i])
    for i in label2:
        if len(data[i]) > max_len2:
            max_len2 = len(data[i])
    for i in label3:
        if len(data[i]) > max_len3:
            max_len3 = len(data[i])
    for i in label4:
        if len(data[i]) > max_len4:
            max_len4 = len(data[i])

    for i in label1:
        if len(data[i]) < max_len1:
            for x in range(max_len1 - len(data[i])):
                data[i].append(0)
    for i in label2:
        if len(data[i]) < max_len2:
            for x in range(max_len2 - len(data[i])):
                data[i].append(0)
    for i in label3:
        if len(data[i]) < max_len3:
            for x in range(max_len3 - len(data[i])):
                data[i].append(0)
    for i in label4:
        if len(data[i]) < max_len4:
            for x in range(max_len4 - len(data[i])):
                data[i].append(0)

    # print("labels:",labels)
    # 生成代表曲线
    represent1 = []
    represent2 = []
    represent3 = []
    represent4 = []

    # print("max_len:", max_len1,' ',max_len2,' ',max_len3,' ',max_len4)
    for i in range(max_len1):
        sum = 0
        for x in label1:
            sum += data[x][i]
        represent1.append(int(sum / len(label1)))

    for i in range(max_len2):
        sum = 0
        for x in label2:
            sum += data[x][i]
        represent2.append(int(sum / len(label2)))

    for i in range(max_len3):
        sum = 0
        for x in label3:
            sum += data[x][i]
        represent3.append(int(sum / len(label3)))

    for i in range(max_len4):
        sum = 0
        for x in label4:
            sum += data[x][i]
        represent4.append(int(sum / len(label4)))

    plt.figure(figsize=(8, 8), dpi=800)
    plt.suptitle("Results for clustering")
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
            title1 += str(sheet_name[x])+' '
        elif labels[x] == 1:
            title2 += str(sheet_name[x])+' '
        elif labels[x] == 2:
            title3 += str(sheet_name[x])+' '
        elif labels[x] == 3:
            title4 += str(sheet_name[x])+' '

    ax1.set_title(title1, fontsize='x-small')
    ax2.set_title(title2, fontsize='x-small')
    ax3.set_title(title3, fontsize='x-small')
    ax4.set_title(title4, fontsize='x-small')

    for i in data:
        x = len(i)-1
        while(x>0):
            if i[x] == 0:
                del i[x]
                x = x-1
            else:
                break

    for x in range(len(labels)):
        if labels[x] == 0:
            ax1.plot(range(len(data[x])), data[x], color="c", linestyle="--")
        elif labels[x] == 1:
            ax2.plot(range(len(data[x])), data[x], color="y", linestyle="--")
        elif labels[x] == 2:
            ax3.plot(range(len(data[x])), data[x], color="b", linestyle="--")
        elif labels[x] == 3:
            ax4.plot(range(len(data[x])), data[x], color="g",  linestyle="--")

    ax1.plot(range(len(represent1)),represent1, color ='m', label='representative curves',  linestyle="-")
    ax1.legend()
    ax2.plot(range(len(represent2)), represent2, color='m', label='representative curves', linestyle="-")
    ax2.legend()
    ax3.plot(range(len(represent3)), represent3, color='m', label='representative curves', linestyle="-")
    ax3.legend()
    ax4.plot(range(len(represent4)), represent4, color='m', label='representative curves', linestyle="-")
    ax4.legend()

    plt.savefig("static/clustering.jpeg")
    '''
    from PIL.WebPImagePlugin import Image
    im = Image.open("static/clustering.jpeg").convert("RGB")
    im.save("static/clustering.webp","webp")
    '''

