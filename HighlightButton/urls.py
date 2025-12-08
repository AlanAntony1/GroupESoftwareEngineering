from django.urls import path
from . import views

urlpatterns = [
    path("toggle-spot/", views.togglespot, name="togglespot"),
]