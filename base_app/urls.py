from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path("3", views.mon, name="don"),
    path('results', views.results, name='results'),
    path('4', views.describe, name='describe'),
    path('data', views.data_delete, name='data_delete')
]
