from django.shortcuts import render, get_object_or_404
from .models import Housing

# Example function to get closest lot info
def get_closest_lot_info(housing):
    # Replace this with your real logic
    return "Lot A", "0.2 miles"

def home(request):
    housing_list = Housing.objects.all()
    selected_housing = None
    closest_lot = None
    distance = None

    housing_id = request.GET.get("housing_id")
    if housing_id:
        selected_housing = get_object_or_404(Housing, id=housing_id)
        closest_lot, distance = get_closest_lot_info(selected_housing)

    context = {
        "housing_list": housing_list,
        "selected_housing": selected_housing,
        "closest_lot": closest_lot,
        "distance": distance,
    }
    return render(request, "housinglotlocater/home.html", context)
