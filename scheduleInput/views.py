from django.shortcuts import render
from .models import ClassInput

# Create your views here.
def schedule(request):
    classes = ClassInput.objects.all()
    return render(request, 'scheduleInput/schedule.html', {"Classes":classes})