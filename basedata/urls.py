from django.urls import path
from . import views

app_name="basedata"

urlpatterns = [
    # 字典类型
    path('basetype/', views.basetype, name='basetype'),
    path('get_datasource/', views.get_datasource, name='get_datasource'),
    path('add/', views.add, name='add'),
    path('edit/', views.edit, name='edit'),
    path('insert/', views.insert, name='insert'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),

    # 数据字典
    path('basedata/', views.basedata, name='basedata'),
    path('getbasedata_datasource/', views.getbasedata_datasource, name='getbasedata_datasource'),
    path('basedata_add/', views.basedata_add, name='basedata_add'),
    path('basedata_insert/', views.basedata_insert, name='basedata_insert'),
    path('basedata_edit/', views.basedata_edit, name='basedata_edit'),
    path('basedata_update/', views.basedata_update, name='basedata_update'),
    path('basedata_delete/', views.basedata_delete, name='basedata_delete')
]