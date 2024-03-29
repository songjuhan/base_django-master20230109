from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path("3", views.mon, name="mon"),
    path('upload', views.upload, name='upload'),
    path('results', views.results, name='results'),
    path('4', views.describe, name='describe'),
    path('null', views.data_null, name='null'),
    path('delete', views.data2,name='delete'),
    path('show', views.show,name='show'),
    path('plot', views.plot,name='plot'),
    path('plot2',views.plot2,name='plot2'),
    path('plot3',views.plot3,name='plot3'),
    path('onehot',views.onehot_encoder,name='onehot_encoder'),
    path('norm',views.Normalization,name='Normalization'),
    path('outlier',views.outlier,name="outlier"),
    path('outlier_results',views.outlier_results, name="outlier_results"),
    path('dbscan',views.dbscan, name="dbscan"),
    path('sub1', views.sub1, name="sub1"),
    path('sub2', views.sub2, name="sub2"),
    path('sub3', views.sub3, name="sub3"),
    path('sub4', views.sub4, name="sub4"),
    path('sub5', views.sub5, name="sub5"),
    path('sub6', views.sub6, name="sub6"),
    path('bar', views.bar, name="bar"),
    path('pie', views.pie, name="pie"),
    path('info', views.info, name="info"),
    path("index", views.index, name="index"),
    path("type", views.type, name="type"),
    path("attribute", views.attribute, name="attribute"),
    path("attribute2", views.attribute2, name="attribute2"),
]
