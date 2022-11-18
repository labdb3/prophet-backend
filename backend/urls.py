from django.urls import path

from . import views

urlpatterns = [
    path("upload", views.upload),
    path("getAllDatasets", views.getAllDatasets),
    path("getDataset",views.getDataset),
    path("deleteData",views.deleteDataSet),
    path("getURL",views.getURL),

    # 模型对比与预测
    path("getAllMetaModels", views.getAllMetaModels),
    #path("getResultOfModel", views.getResultOfModel),
    path("loadModel_multi",views.loadModel_multi),

    # 数据预处理
    path("getAllPreprocessMethods",views.getAllPreprocessMethods),
    path("getResultOfPreprocess",views.getResultOfPreprocess),
    path("saveDataset",views.saveDataset),

    # 模型调优
    path("saveModel",views.saveModel),
    path("getSavedModels",views.getModelList),
    path("loadModel",views.loadModel),
    path("getResultWithParams",views.getResultWithParams),

    # 模型删除
    path("deleteModel",views.deleteModel),

    # 聚类展示
    path("showPhoto",views.showPhoto),
    path("clustering",views.showClustering),
    path("getSumFitting",views.getSumFitting)
]
