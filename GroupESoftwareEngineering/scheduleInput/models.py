from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class ClassInput(models.Model):
    name = models.CharField(max_length = 10)
    startTime = models.TimeField()
    endTime = models.TimeField()
    days = models.CharField(max_length = 10)
    location = models.TextField()

    def clean(self):
        """Ensure that startTime is before endTime."""
        if self.startTime and self.endTime and self.startTime >= self.endTime:
            raise ValidationError("Start time must be before end time.")

    def __str__(self):
        return self.name
