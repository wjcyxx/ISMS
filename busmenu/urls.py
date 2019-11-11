from django.urls import path
from . import views

app_name="busmenu"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('get_treedatasource/', views.get_treedatasource.as_view(), name='get_treedatasource'),
    path('get_refdatasource/', views.get_refdatasource.as_view(), name='get_refdatasource'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource')

]