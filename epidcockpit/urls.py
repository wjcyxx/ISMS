from django.urls import path
from . import views

app_name="epidcockpit"

urlpatterns = [
    path('epidcockpit_entrance/', views.epidcockpit_entrance.as_view(), name='epidcockpit_entrance'),
]