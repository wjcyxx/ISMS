from django.urls import path
from . import views

app_name="datacockpit"

urlpatterns = [
    path('get_datacockpit/', views.get_datacockpit.as_view(), name='get_datacockpit')

]
