from django.urls import path
from . import views

app_name="device"

urlpatterns = [
    path('device/', views.device, name='device'),
    path('get_datasource/', views.get_datasource, name='get_datasource'),
    path('add/', views.add, name='add'),
    path('edit/', views.edit, name='edit'),
    path('insert/', views.insert, name='insert'),
    path('disable/', views.disabled, name='disabled'),
    path('add_callinterface/', views.add_callinterface.as_view(), name='add_callinterface'),
    path('insert_callinterface/', views.insert_callinterface.as_view(), name='insert_callinterface'),
    path('get_callinterface_datasource/', views.get_callinterface_datasource.as_view(), name='get_callinterface_datasource')
]