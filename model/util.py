import numpy as np


##BASE_DIR = '/Users/zongdianliu/python/prophet-backend/data/datasets'



def log(data):
    data = np.log1p(data)
    return data


def antilog(data):
    data = np.exp(data) - 1
    return data


def standard(data):
    data = (data - data.mean()) / (data.std())
    return data


def anti_standard(data):
    data = data*data.std()+data.mean()
    return data


def normalize(data):
    data = (data-data.min())/(data.max()-data.min())
    return data


def anti_normalize(data):
    data = data*(data.max()-data.min())+data.min()
    return data


def nihe_error(y_true, y_pred):
    nihe_error = 0
    count = 0
    for i in range(len(y_true)):
        if y_pred[i] != 0 and y_true[i] != 0:
            nihe_error += y_pred[i] / y_true[i]
            count += 1
    nihe_error = nihe_error / count
    return nihe_error



import pandas as pd

def prophet_preprocess(data):
    data.columns = ['ds','y']
    i = 0
    while (i<(len(data['y'].values)-2)):
        # print(i)
        if data['y'].values[i]==0 or data['y'].values[i]==1:
            temp = i
            while(data['y'].values[i+1]==0 or data['y'].values[i+1]==1):
                i += 1
            # print(temp, i)
            if temp == i:
                if i == 0:
                    data['y'].values[0] = 2/5*data['y'].values[1]
                    # print(data['y'].values[0])
                    data['y'].values[1] = 3 / 5 * data['y'].values[1]
                elif i == len(data['y'].values)-1:
                    data['y'].values[i] = 2 / 5 * data['y'].values[i-1]
                    data['y'].values[i-1] = 3 / 5 * data['y'].values[i-1]
                else:
                    if data['y'].values[i-1] > data['y'].values[i+1]:
                        data['y'].values[i + 1]= (data['y'].values[i-1]+data['y'].values[i+1])/3 - (data['y'].values[i-1]-data['y'].values[i+1])/6
                        data['y'].values[i]= (data['y'].values[i-1]+data['y'].values[i+1])/3
                        data['y'].values[i - 1]=(data['y'].values[i-1]+data['y'].values[i+1])/3 + (data['y'].values[i-1]-data['y'].values[i+1])/6
                    elif data['y'].values[i-1] <= data['y'].values[i+1]:
                        data['y'].values[i + 1] = (data['y'].values[i-1]+data['y'].values[i+1])/3 + (data['y'].values[i+1]-data['y'].values[i-1])/6
                        data['y'].values[i] = (data['y'].values[i - 1] + data['y'].values[i + 1]) / 3
                        data['y'].values[i - 1] = (data['y'].values[i - 1] + data['y'].values[i + 1]) / 3 - (data['y'].values[i + 1] - data['y'].values[i - 1]) / 6
            elif temp != i:
                if temp == 0:
                    data['y'].values[temp] = (data['y'].values[i+1]-(i-temp+2)*data['y'].values[i+1]/6)/(i-temp+2)
                    for j in range(temp+1,i+2):
                        data['y'].values[j] = data['y'].values[temp]+(j-temp)*data['y'].values[i+1]/(i-temp+1)/3
                elif i == len(data['y'].values)-1:
                    data['y'].values[i] = (data['y'].values[temp-1]-(i-temp+2)*data['y'].values[temp-1]/6)/(i-temp+2)
                    for j in range(temp-1,i):
                        data['y'].values[j] = data['y'].values[i] + (i-j)*data['y'].values[temp-1]/(i-temp+1)/3
                else:
                    if data['y'].values[temp-1] > data['y'].values[i+1]:
                        data['y'].values[i+1] = (data['y'].values[temp - 1]+data['y'].values[i+1]-(i-temp+3)*(data['y'].values[temp-1]-data['y'].values[i+1])/6)/(i-temp+3)

                        for j in range(temp-1,i+1):
                            data['y'].values[j] = data['y'].values[i+1] + (i+1-j)*(data['y'].values[temp-1]-data['y'].values[i+1])/3/(i-temp+2)
                    elif data['y'].values[temp-1] <= data['y'].values[i+1]:
                        data['y'].values[temp - 1] = (data['y'].values[temp - 1]+data['y'].values[i+1]-(i-temp+3)*(data['y'].values[i+1]-data['y'].values[temp-1])/6)/(i-temp+3)
                        for j in range(temp,i+2):
                            data['y'].values[j]= data['y'].values[temp - 1]+(j-temp+1)*(data['y'].values[i+1]-data['y'].values[temp-1])/3/(i-temp+2)
        i += 1
    print(type(data))
    return data
# writer = pd.ExcelWriter(r'./data.xlsx', engine = 'xlsxwriter')
'''
if __name__=='__main__':
    data = pd.read_excel("/Users/zongdianliu/python/prophet-backend/data/datasets/数据单元.xlsx", sheet_name='1',header=0,skiprows=0)
    print(data)
    data= preprocess(data)
    print(data)
    #     data.to_excel(writer, sheet_name = str(i))
    # writer.save()
    # writer.close()
'''
