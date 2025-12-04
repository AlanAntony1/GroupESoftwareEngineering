from django.urls import path
from . import views

urlpatterns = [
    path("", views.housing_view, name='housing_lot_locater'),
    path("housing/<int:housing_id>/", views.housing_details, name='housing_details'),
]
