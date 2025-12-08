from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Highlight(models.Model):
    spotid = models.CharField(max_length=200,default="",unique=True)
    isHighlighted = models.BooleanField(default=False)
    lastPressed= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.spotid} - {'Highlighted' if self.isHighlighted else 'Normal'}"