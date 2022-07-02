from django.urls import path

from . import views

urlpatterns = [
    path("upload", views.upload),
    path("index", views.index),
    path("getAllModels", views.getAllModels),
    path("getAllDatasets", views.getAllDatasets),
    path("getResultOfModel", views.getResultOfModel),
    path("getDataset",views.getDataset)
]
