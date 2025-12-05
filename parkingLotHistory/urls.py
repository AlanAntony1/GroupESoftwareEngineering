from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.parking_history, name='parking_history'),
]


#from django.urls import path
#from . import views

#urlpatterns = [
 #   path('history/', views.parking_history, name='parking_history'),
  #  path('add_history/', views.add_history, name='add_history'),
#]
