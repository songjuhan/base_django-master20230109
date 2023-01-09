from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path("3", views.mon, name="don"),
    path('results', views.results, name='results'),
]
