from django.shortcuts import render, get_object_or_404
from .models import Housing

# Dummy closest lot info
def get_closest_lot_info(housing):
    example_info = {
        "Cross Village": ("Lot A", "0.5 miles"),
        "McCasland Hall": ("Lot B", "0.3 miles"),
        "South Building": ("Lot C", "0.4 miles"),
        "Couch Center": ("Lot D", "0.6 miles"),
        "Walker Center": ("Lot E", "0.2 miles"),
        "Residential Colleges (Dunham & Headington College)": ("Lot F", "0.7 miles"),
        "David L. Boren Hall": ("Lot G", "0.5 miles"),
        "Headington Hall": ("Lot H", "0.4 miles"),
        "Traditions Square": ("Lot I", "0.6 miles"),
        "Kraettli Apartments": ("Lot J", "0.3 miles"),
    }
    return example_info.get(housing.name, ("Unknown", "--"))

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
