from django.urls import path
from . import views

app_name="envrule"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource'),
    path('add/', views.add.as_view(), name='add'),
    path('edit/', views.edit.as_view(), name='edit'),
    path('insert/', views.insert.as_view(), name='insert'),
    path('disabled/', views.disabled.as_view(), name='disabled'),
    path('add_switch/', views.add_switch.as_view(), name='add_switch'),
    path('insert_switch/', views.insert_switch.as_view(), name='insert_switch'),
    path('get_switch_datasource/', views.get_switch_datasource.as_view(), name='get_switch_datasource'),
    path('delete_switch/', views.delete_switch.as_view(), name='delete_switch')

]