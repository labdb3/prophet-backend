from django.urls import path

from . import views

urlpatterns = [
    path("upload", views.upload),
    path("saveTag",views.saveTag),
    path("getTagData",views.getTagData),
    path("getAllDatasets", views.getAllDatasets),
    path("getDataset",views.getDataset),

    # 模型对比与预测
    path("getAllMetaModels", views.getAllMetaModels),
    path("getResultOfModel", views.getResultOfModel),
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
]
