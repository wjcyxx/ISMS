from django.urls import path
from . import views

app_name="ismsapi"

urlpatterns = [
    path('get_token/', views.get_token.as_view(), name='get_token')

]