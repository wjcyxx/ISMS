from django.urls import path
from . import views
from . import tests

app_name="devinterfacesrv"

urlpatterns = [
    path('runservice/', tests.runservice, name='runservice'),
    path('devservice/', views.devservice, name='devservice'),
]
