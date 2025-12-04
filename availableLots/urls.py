from django.urls import path
from . import views

urlpatterns = [
    path("", views.requestLots, name="available_lots"),
    path("<int:lot_id>/update/", views.update_lot_availability, name="update_lot"),
]
