from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.parking_history, name='parking_history'),
    #path('add-housing-history/', views.add_housing_history, name='add_housing_history'),
]
