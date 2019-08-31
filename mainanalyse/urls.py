from django.urls import path
from . import views

app_name="mainanalyse"

urlpatterns = [
    path('topanalyse/', views.topanalyse.as_view(), name='topanalyse'),
    path('pedpassageanlayse/', views.pedpassageanlayse.as_view(), name='pedpassageanlayse')

]