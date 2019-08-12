from django.urls import path
from . import views

app_name="abnpound"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource'),
    path('add/', views.add.as_view(), name='add'),
    path('insert/', views.insert.as_view(), name='insert')

]