from django.urls import path
from . import views

app_name="menchanical"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource'),
    path('add/', views.add.as_view(), name='add'),
    path('edit/', views.edit.as_view(), name='edit'),
    path('insert/', views.insert.as_view(), name='insert'),
    path('disabled/', views.disabled.as_view(), name='disabled'),
    path('add_auth/', views.add_auth.as_view(), name='add_auth'),
    path('insert_auth/', views.insert_auth.as_view(), name='insert_auth'),
    path('get_operauth_datasource/', views.get_operauth_datasource.as_view(), name='get_operauth_datasource'),
    path('get_operlog_datasource/', views.get_operlog_datasource.as_view(), name='get_operlog_datasource')
]