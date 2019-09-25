from django.urls import path
from . import views

app_name="passagerecord"

urlpatterns = [
    path('passagerecord/', views.passagerecord, name='passagerecord'),
    path('get_datasource/', views.get_datasource, name='get_datasource')
]