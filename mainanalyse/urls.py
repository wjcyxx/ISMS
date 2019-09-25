from django.urls import path
from . import views

app_name="mainanalyse"

urlpatterns = [
    path('topanalyse/', views.topanalyse.as_view(), name='topanalyse'),
    path('pedpassageanlayse/', views.pedpassageanlayse.as_view(), name='pedpassageanlayse'),
    path('vehpassageanalyse/', views.vehpassageanalyse.as_view(), name='vehpassageanalyse'),
    path('get_pedpassage_news/', views.get_pedpassage_news.as_view(), name='get_pedpassage_news'),
    path('get_vehpassage_news/', views.get_vehpassage_news.as_view(), name='get_vehpassage_news'),
    path('envanalyse/', views.envanalyse.as_view(), name='envanalyse')
]