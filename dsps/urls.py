from django.urls import path
from . import views

app_name="dsps"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource'),
    path('dev_setupinfo/', views.dev_setupinfo.as_view(), name='dev_setupinfo'),
    path('get_dev_datasource/', views.get_dev_datasource.as_view(), name='get_dev_datasource')
]