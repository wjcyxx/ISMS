from django.urls import path
from . import views

app_name="hatrule"

urlpatterns = [
    path('hatrule/', views.hatrule.as_view(), name='hatrule'),
    path('get_datasourcea/', views.get_datasourcea.as_view(), name='get_datasourcea')

]