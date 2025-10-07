from django.urls import path
from . import views

urlpatterns = [
    path("", views.building_view, name = 'locater'),
    path("building/<int:building_id>/", views.building_details, name='building_details'),
]