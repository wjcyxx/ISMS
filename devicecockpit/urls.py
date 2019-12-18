from django.urls import path
from . import views

app_name="devicecockpit"

urlpatterns = [
    path('envcockpit_entrance/', views.envcockpit_entrance.as_view(), name='envcockpit_entrance'),
    path('get_envrealtimedata/', views.get_envrealtimedata.as_view(), name='get_envrealtimedata'),
    path('get_envhisdata/', views.get_envhisdata.as_view(), name='get_envhisdata'),
    path('get_area_analyse/', views.get_area_analyse.as_view(), name='get_area_analyse'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource')
]