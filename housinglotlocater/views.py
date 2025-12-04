from django.shortcuts import render
from .models import Housing

def home(request):
    housing_list = Housing.objects.all()
    return render(request, "housinglotlocater/home.html", {"housing_list": housing_list})
