from django.urls import path
from . import views

app_name = "datadashboard"

urlpatterns = [
    path("", views.home, name="dashboard"),
    path("data.json", views.data_json, name="dashboard_json"),  # optional
]

