from django.urls import path
from . import views

app_name="devinterfacesrv"

urlpatterns = [
    path('runservice/', views.runservice, name='runservice'),
    path('devservice/', views.devservice, name='devservice'),
]
