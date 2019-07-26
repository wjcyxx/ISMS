from django.urls import path
from . import views

app_name="hatrule"

urlpatterns = [
    path('hatrule/', views.hatrule.as_view(), name='hatrule'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource'),
    path('add/', views.add.as_view(), name='add')

]