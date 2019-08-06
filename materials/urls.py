from django.urls import path
from . import views

app_name="materials"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource'),
    path('get_treedatasource/', views.get_treedatasource.as_view(), name='get_treedatasource'),
    path('get_refdatasource/', views.get_refdatasource.as_view(), name='get_refdatasource'),
    path('add/', views.add.as_view(), name='add'),
    path('edit/', views.edit.as_view(), name='edit'),
    path('insert/', views.insert.as_view(), name='insert'),
]