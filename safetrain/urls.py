from django.urls import path
from . import views

app_name="safetrain"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource'),
    path('add/', views.add.as_view(), name='add'),
    path('edit/', views.edit.as_view(), name='edit'),
    path('insert/', views.insert.as_view(), name='insert'),
    path('get_selperson_datasource/', views.get_selperson_datasource.as_view(), name='get_selperson_datasource'),
    path('selperson/', views.selperson.as_view(), name='selperson'),
    path('insert_selperson/', views.insert_person.as_view(), name='insert_selperson')

]