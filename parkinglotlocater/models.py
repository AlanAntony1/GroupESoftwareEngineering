from django.db import models

# Create your models here.
class Building(models.Model):
    buildingName = models.CharField(max_length=100)
    closestLot = models.TextField()
    distance = models.DecimalField(max_digits = 5, decimal_places  = 2, default = 0.0)
    parkingLotLat = models.DecimalField(max_digits = 16, decimal_places = 13, default = 0.0)
    parkingLotLong = models.DecimalField(max_digits = 16, decimal_places = 13, default = 0.0)
    

    def __str__(self):
        return self.buildingName
    
    def getDistance(self):
        return self.distance

# Aditi Model
class Housing(models.Model):
    housingName = models.CharField(max_length = 100)
    closestParking = models.CharField(max_length = 100)
    distance = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0.0)

    def __str__(self):
        return self.housingName
    
    def getDistance(self):
        return self.distance
