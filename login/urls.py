from django.urls import path
from login import views

app_name="login"

urlpatterns = [
    path('index/', views.index, name='login'),
    # path('login_chk/', views.login_chk, name='login_chk'),
    # path('login_ok/', views.login_ok, name='login_ok'),
]