from django.urls import path
from . import views

app_name="pedpassage"

urlpatterns = [
    path('pedpassage/', views.pedpassage, name='pedpassage'),
    path('get_datasource/', views.get_datasource, name='get_datasource'),
    path('add/', views.add, name='add'),
    path('edit/', views.edit, name='edit'),
    path('insert/', views.insert, name='insert'),
    path('disable/', views.disabled, name='disabled'),
]