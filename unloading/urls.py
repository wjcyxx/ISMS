from django.urls import path
from . import views

app_name="unloading"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource'),
    path('get_run_datasource/', views.get_run_datasource.as_view(), name='get_run_datasource')
]