import numpy as np
import pandas as pd
data = pd.read_excel("./数据单元.xlsx", sheet_name='3',header=0,skiprows=0)

def preprocess(data):
    data.columns = ['y']
    i = 0
    while (i<(len(data['y'].values)-2)):
        if data['y'].values[i]==0 or data['y'].values[i]==1:
            temp = i
            while(data['y'].values[i+1]==0 or data['y'].values[i+1]==1):
                i += 1
            if temp == i:
                if i == 0:
                    data['y'].values[0] = 2/5*data['y'].values[1]
                    print(data['y'].values[0])
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
    return data

from common.common import *
import pandas as pd
from data.preprocess import Method2


if __name__=='__main__':
    all_data = LoadDataBase()
    sheetname = []
    data = []
    x = []
    for fileName in all_data.keys():
        for sheetName in all_data[fileName]:
            sheetname.append(fileName + "-" + sheetName)
            data.append(all_data[fileName][sheetName]["yAxis"])
            x.append(all_data[fileName][sheetName]["xAxis"])

    res =[]
    for item in data:
        item = pd.DataFrame(np.array(item).reshape((-1,1)))
        item = preprocess(item).to_numpy().transpose().tolist()
        res.append(item[0])

    dump_data = {}
    for size in [2,3,4,5,6,7,8]:
        for idx,item in enumerate(res):
            print(x[idx],item)
            _data = Method2([x[idx],item],size)
            name = sheetname[idx]+":"+str(size)
            dump_data[name]=_data

    json.dump(dump_data,open("dump_data.json","w",encoding='utf-8'),ensure_ascii=False)
