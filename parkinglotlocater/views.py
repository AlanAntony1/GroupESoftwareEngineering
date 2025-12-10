from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Building
from HighlightButton.models import Highlight 
import json

# Create your views here.
def building_view(request):
    
    ##Highlightbutton because we cant push two returns
    highlighted = Highlight.objects.filter(isHighlighted=True)
    highlighted_ids = [h.spotid for h in highlighted]
    highlighted_json = json.dumps(highlighted_ids)
    
    buildings = Building.objects.all()
    return render(request, 'parkinglotlocater/locater.html', {
        "highlighted_spots_json": highlighted_json,
        "buildings": buildings,
    })

def building_details(request, building_id):
    building = get_object_or_404(Building, id = building_id)
    data = {
        "closestLot": building.closestLot,
        "distance": str(building.distance),
        "parkingLotLat": float(building.parkingLotLat),
        "parkingLotLong": float(building.parkingLotLong)
    }
    return JsonResponse(data)