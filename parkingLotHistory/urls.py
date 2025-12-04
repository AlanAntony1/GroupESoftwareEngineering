from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.parking_history, name='parking_history'),
]
