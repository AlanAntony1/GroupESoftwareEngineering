#from django.db import models

#class ParkingHistory(models.Model):
 #   lot_name = models.CharField(max_length=100)
  #  occupied_spots = models.IntegerField()
  #  available_spots = models.IntegerField()
  #  timestamp = models.DateTimeField(auto_now_add=True)

  #  def __str__(self):
   #     return f"{self.lot_name} at {self.timestamp}"



#class HousingHistory(models.Model):
#    building_name = models.CharField(max_length=255)
#    timestamp = models.DateTimeField(auto_now_add=True)

  #  def __str__(self):
  #      return f"{self.building_name} at {self.timestamp}"



from django.db import models
from django.contrib.auth.models import User  # optional if you want per-user history

class ParkingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # optional
    building_name = models.CharField(max_length=100)
    closest_lot = models.TextField()
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.building_name} – {self.closest_lot} – {self.distance} miles"
