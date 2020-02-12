from django.urls import path
from . import views

app_name="mapview"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('get_project/', views.get_project.as_view(), name='get_project'),
    path('show_projectdetail/', views.show_projectdetail.as_view(), name='show_projectdetail')
]