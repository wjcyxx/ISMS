from django.urls import path
from . import views

app_name="vehiclegate"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource'),
    path('add/', views.add.as_view(), name='add'),
    path('edit/', views.edit.as_view(), name='edit'),
    path('insert/', views.insert.as_view(), name='insert'),
    path('disabled/', views.disabled.as_view(), name='disabled'),
    path('add_sigin/', views.add_sigin.as_view(), name='add_sigin'),
    path('insert_sigin/', views.insert_sigin.as_view(), name='insert_sigin'),
    path('get_sigin_datasource/', views.get_sigin_datasource.as_view(), name='get_sigin_datasource'),
    path('delete_sigin/', views.delete_sigin.as_view(), name='delete_sigin')
]