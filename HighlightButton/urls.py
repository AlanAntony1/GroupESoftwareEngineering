from django.urls import path
from . import views

urlpatterns = [
    path("toggle-spot/", views.toggle_spot, name="toggle_spot"),
]