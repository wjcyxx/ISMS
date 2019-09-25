from django.urls import path
from . import views

app_name="personnel"

urlpatterns = [
    path('personnel/', views.personnel, name='personnel'),
    path('get_datasource/', views.get_datasource, name='get_datasource'),
    path('add/', views.add, name='add'),
    path('edit/', views.edit, name='edit'),
    path('insert/', views.insert, name='insert'),
    path('disable/', views.disabled, name='disabled'),
    path('sign/', views.sign, name='sign'),
    path('show_upload/', views.show_upload, name='show_upload'),
    path('get_certificate/', views.get_certificate, name='get_certificate'),
    path('showTrain_upload/', views.showTrain_upload, name='showTrain_upload'),
    path('showPhoto_upload/', views.showPhoto_upload, name='showPhoto_upload'),
    path('get_safetrain/', views.get_safetrain, name='get_safetrain')

]