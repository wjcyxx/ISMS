from django.urls import path
from . import views

app_name="devicecockpit"

urlpatterns = [
    path('envcockpit_entrance/', views.envcockpit_entrance.as_view(), name='envcockpit_entrance'),
    path('get_envrealtimedata/', views.get_envrealtimedata.as_view(), name='get_envrealtimedata')
]