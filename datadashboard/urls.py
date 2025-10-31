from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dashboard-home'),
    path('data.json', views.data_json, name='dashboard-data'),
]
