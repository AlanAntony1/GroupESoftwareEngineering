from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="housing_lot_locater"),
]
