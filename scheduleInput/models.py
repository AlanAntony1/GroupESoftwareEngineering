from django.db import models

# Create your models here.
class ClassInput(models.Model):
    name = models.CharField(max_length = 10)
    time = models.TimeField()
    duration = models.DurationField()
    days = models.CharField(max_length = 10)
    location = models.TextField()

def __str__(self):
    return self.name


