from django.urls import path
from . import views

app_name="organize"

urlpatterns = [
    path('organize/', views.organize, name='organize'),
    path('get_datasource/', views.get_datasource, name='get_datasource'),
    path('add/', views.add, name='add'),
    path('edit/', views.edit, name='edit'),
    path('insert/', views.insert, name='insert'),
    path('disable/', views.disabled, name='disabled'),
    path('show_upload/', views.show_upload, name='show_upload'),
    path('get_quailfications/', views.get_quailfications, name='get_quailfications'),
    path('delete/', views.delete, name='delete'),
]
