from django.urls import path
from . import views

app_name="personinfomap"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('groupanalyse/', views.groupanalyse.as_view(), name='groupanalyse'),
    path('attenanalyse/', views.attenanalyse.as_view(), name='attenanalyse')
]