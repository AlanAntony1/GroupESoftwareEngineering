from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Highlight(models.Model):
    button = models.BooleanField(default= False)
    isHighlighted = models.BooleanField(default=False)
    lastPressed= models.DateTimeField(auto_now=True)
   # label = models.CharField(max_length=50, default="Faculty Only Highlighter")
#hello

    def press_button(self):
        self.button = True
        self.isHighlighted = not self.isHighlighted  
        self.lastPressed  = timezone.now()
        self.save()


    def __str__(self):
        return f"{self.label} - {'On' if self.isHighlighted else 'Off'}"