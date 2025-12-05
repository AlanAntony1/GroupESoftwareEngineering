from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Housing

# Main page view
def housing_view(request):
    housings = Housing.objects.all()
    return render(request, 'housinglotlocater/home.html', {"housings": housings})

# API endpoint to return closest parking info
def housing_details(request, housing_id):
    housing = get_object_or_404(Housing, id=housing_id)
    data = {
        "closestParking": housing.closestParking,
        "distance": str(housing.distance)
    }
    return JsonResponse(data)
