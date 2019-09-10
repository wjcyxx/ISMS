from django.urls import path
from . import views

app_name="mapview"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance')

]