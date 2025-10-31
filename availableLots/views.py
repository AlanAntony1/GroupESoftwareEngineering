from django.shortcuts import render
from .models import AvailableLots

# Create your views here.
def requestLots(request):
    Lots = AvailableLots.objects.all()
    return render(req, 'availableLots/AvailableLots.html')