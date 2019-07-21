from django.urls import path
from . import views

app_name="devinterface"

urlpatterns = [
    path('devinterface/', views.devinterface, name='devinterface'),
    path('get_datasource/', views.get_datasource, name='get_datasource'),
    path('add/', views.add, name='add'),
    path('edit/', views.edit, name='edit'),
    path('insert/', views.insert, name='insert'),
    path('disable/', views.disabled, name='disabled'),
    path('addparam/', views.addparam, name='addparam'),
    path('param_insert/', views.param_insert, name='param_insert')
]