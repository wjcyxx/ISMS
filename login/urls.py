from django.urls import path
from login import views

app_name="login"

urlpatterns = [
    path('index/', views.index, name='login'),
    path('login_chk/', views.login_chk, name='login_chk'),
    path('login_showPrj/', views.login_showPrj, name='login_showPrj'),
    path('get_project/', views.get_project, name='get_project'),
    path('login_ok/', views.login_ok, name='login_ok'),
    path('login_ok/show/', views.show, name='show'),
]