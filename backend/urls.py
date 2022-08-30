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


    # 模型调优
    path("saveModel",views.saveModel),
    path("getSavedModels",views.getModelList),
    path("loadModel",views.loadModel),
    path("getResultWithParams",views.getResultWithParams),
]
