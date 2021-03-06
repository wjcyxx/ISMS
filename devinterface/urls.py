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
    path('editparam/', views.editparam, name='editparam'),
    path('param_insert/', views.param_insert, name='param_insert'),
    path('get_paramdatasource/', views.get_paramdatasource, name='get_paramdatasource'),
    path('param_delete/', views.param_delete, name='param_delete'),
    path('subinterface_add/', views.subinterface_add.as_view(), name='subinterface_add'),
    path('subinterface_insert/', views.subinterface_insert.as_view(), name='subinterface_insert'),
    path('get_subinterface_datasource/', views.get_subinterface_datasource.as_view(), name='get_subinterface_datasource'),
    path('del_subint/', views.del_subint.as_view(), name='del_subint')
]