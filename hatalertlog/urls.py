from django.urls import path
from . import views

app_name="hatalertlog"

urlpatterns = [
    path('enterance/', views.enterance.as_view(), name='enterance'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource'),

]