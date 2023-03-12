import os
import json
import pandas as pd


"""
    # 数据存放格式
    {
        "file_name":{
            "sheet_name":{
                            "xAxis":[],
                            "yAxis":[],
                         }
        }
    }
"""
URL = "http://127.0.0.1:8000/"
#DATABASE_PATH = "/Users/zongdianliu/python/prophet-backend/data"
DATABASE_PATH = "D:\dblab3\prophet-backend\data"

def getFileName(query):
    fileName = query.split("_")[0]
    sheetName = "_".join(query.split("_")[1:])
    return fileName,sheetName


def LoadDataBase():
    f = open(os.path.join(DATABASE_PATH, "dataset.json"), 'r', encoding='utf-8')
    all_data = json.load(f)
    f.close()
    return all_data

def DumpDataBase(all_data):
    f = open(os.path.join(DATABASE_PATH, "dataset.json"), 'w', encoding='utf-8')
    json.dump(all_data, f, ensure_ascii=False)
    f.close()

def GetDataFrame_dataset(fileName,sheetName,col1,col2):
    all_data = LoadDataBase()
    data = {
        col1:all_data[fileName][sheetName]["xAxis"],
        col2:all_data[fileName][sheetName]["yAxis"]
    }
    return pd.DataFrame(data)


def GetData(dataset):
    fileName, sheetName = getFileName(dataset)
    all_data = LoadDataBase()
    data = [all_data[fileName][sheetName]["xAxis"], all_data[fileName][sheetName]["yAxis"]]
    return data
