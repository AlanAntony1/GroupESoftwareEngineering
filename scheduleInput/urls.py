from django.urls import path
from . import views


urlpatterns = [
    path("", views.schedule, name="schedule"),
    path("delete/<int:pk>/", views.delete_class, name="delete_class"),
]