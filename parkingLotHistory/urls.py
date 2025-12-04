from django.urls import path
from . import views

urlpatterns = [
    path('add_history/', views.add_history, name='add_history'),
    path('history/', views.parking_history, name='parking_history'),
]
