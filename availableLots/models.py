from django.db import models

# Create your models here.

class AvailableLots(models.Model):
    lot_id = models.AutoField(primary_key=True)
    lot_name = models.CharField(max_length=100)
    total_spaces = models.PositiveIntegerField()
    available_spaces = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='Open')
    last_updated = models.DateTimeField(auto_now=True)

    def update_availability(self, new_count):
        """Update available spaces and status."""
        self.available_spaces = new_count
        self.status = 'Full' if new_count == 0 else 'Open'
        self.save()

    def occupancy_rate(self):
        """Return how full the lot is as a percentage."""
        if self.total_spaces == 0:
            return 0
        return round((1 - self.available_spaces / self.total_spaces) * 100, 2)

    def __str__(self):
        return f"{self.lot_name} - {self.status} ({self.available_spaces}/{self.total_spaces})"