from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Building

# Create your views here.
def building_view(request):
    buildings = Building.objects.all()
    return render(request, 'parkinglotlocater/locater.html', {"buildings": buildings})

def building_details(request, building_id):
    building = get_object_or_404(Building, id = building_id)
    data = {
        "closestLot": building.closestLot,
        "distance": str(building.distance)
    }
    return JsonResponse(data)