from django.urls import path
from . import views

app_name="team"

urlpatterns = [
    path('team/', views.team, name='team'),
    path('get_datasource/', views.get_datasource, name='get_datasource'),
    path('get_workdatasource/', views.get_workdatasource, name='get_workdatasource'),
    path('add/', views.add, name='add'),
    path('edit/', views.edit, name='edit'),
    path('insert/', views.insert, name='insert'),
    path('disable/', views.disabled, name='disabled'),
]