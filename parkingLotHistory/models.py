from django.db import models
from django.contrib.auth.models import User

#class ParkingHistory(models.Model):
 #   lot_name = models.CharField(max_length=100)
   # occupied_spots = models.IntegerField()
    #available_spots = models.IntegerField()
   # timestamp = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
    #    return f"{self.lot_name} at {self.timestamp}"

def setUp(self):
    super().setUp()
    # Create a test user
    user = User.objects.create(username="testuser")
    # Add a test parking history
    ParkingHistory.objects.create(
        user=user,
        lot_name="Lot A",
        occupied_spots=5,
        available_spots=10
    )


#class ParkingHistory(models.Model):
 #   user = models.ForeignKey(User, on_delete=models.CASCADE)
   # building_name = models.CharField(max_length=255)
    #timestamp = models.DateTimeField(auto_now_add=True)

#    def __str__(self):
  #      return f"{self.user.username} - {self.building_name} @ {self.timestamp}"
