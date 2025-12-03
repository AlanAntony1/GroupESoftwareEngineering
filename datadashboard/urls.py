from django.urls import path
from . import views

app_name = "datadashboard"

urlpatterns = [
    path("", views.home, name="dashboard"),   # <-- use home, not dashboard
]
