from django.db import models

class ParkingHistory(models.Model):
    lot_name = models.CharField(max_length=100)
    occupied_spots = models.IntegerField()
    available_spots = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lot_name} at {self.timestamp}"




#class ParkingHistory(models.Model):
 #   user = models.ForeignKey(User, on_delete=models.CASCADE)
   # building_name = models.CharField(max_length=255)
    #timestamp = models.DateTimeField(auto_now_add=True)

#    def __str__(self):
  #      return f"{self.user.username} - {self.building_name} @ {self.timestamp}"
