from django.urls import path
from . import views

app_name="personauth"

urlpatterns = [
    path('add/', views.add, name='add'),
    path('auth/', views.auth, name='auth')
]