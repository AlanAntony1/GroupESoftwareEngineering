# datadashboard/urls.py
from django.urls import path
from . import views

app_name = "datadashboard"

urlpatterns = [
    path("", views.home, name="dashboard-home"),      # /dashboard/
    path("data.json", views.data_json, name="dashboard-data"),
    path("ping/", views.ping, name="ping"),           # /dashboard/ping/
]




