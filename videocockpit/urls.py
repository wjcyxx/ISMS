from django.urls import path
from . import views

app_name="videocockpit"

urlpatterns = [
    path('videocockpit_entrance/', views.videocockpit_entrance.as_view(), name='videocockpit_entrance'),


]