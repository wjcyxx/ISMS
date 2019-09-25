from django.urls import path
from . import views

app_name="busmenu"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('get_treedatasource/', views.get_treedatasource.as_view(), name='get_treedatasource'),
]