from django.db import models

class ParkingLot(models.Model):
    name = models.CharField(max_length=100)
    total_spaces = models.PositiveIntegerField()
    occupied_spaces = models.PositiveIntegerField(default=0)

    @property
    def available_spaces(self):
        return self.total_spaces - self.occupied_spaces

    def __str__(self):
        return f"{self.name} ({self.available_spaces} free)"
