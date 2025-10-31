from django.shortcuts import render
from django.http import JsonResponse
from parkinglotlocater.models import Building

def home(request):
    buildings = Building.objects.all().order_by('buildingName')

    labels = [b.buildingName for b in buildings]
    distances = [float(b.distance) for b in buildings]

    context = {
        "title": "OU Parking — Dashboard",
        "total_buildings": buildings.count(),
        "buildings": buildings,
        "labels": labels,
        "distances": distances,
    }
    return render(request, "datadashboard/home.html", context)

def data_json(request):
    buildings = Building.objects.all().order_by('buildingName')
    data = {
        "labels": [b.buildingName for b in buildings],
        "distances": [float(b.distance) for b in buildings],
    }
    return JsonResponse(data)

