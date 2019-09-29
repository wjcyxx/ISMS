from django.urls import path
from . import views

app_name="personauth"

urlpatterns = [
    path('add/', views.add, name='add'),
    path('auth/', views.auth, name='auth'),
    path('makeiccard_add/', views.makeiccard_add.as_view(), name='makeiccard_add'),
    path('makeiccard/', views.makeiccard.as_view(), name='makeiccard')
]