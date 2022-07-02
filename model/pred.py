from .model import *
from prophet.config import *
import os

def getResultOfDataset_prophet(dataset):
    data = pd.read_excel(os.path.join(BASE_DIR, dataset), header=0, skiprows=0).to_numpy().transpose().tolist()
    model = prophet()
    model.fit(data[0], data[1])
    predict = model.predict(data[0][0], len(data[0]), 5)
    return predict.to_numpy().tolist()
