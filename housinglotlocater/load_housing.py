from .models import Housing

def load_housing():
    housing_list = [
        {"name": "Cross Village", "lot": "Lot A", "distance": 0.5},
        {"name": "McCasland Hall", "lot": "Lot B", "distance": 0.3},
        {"name": "South Building", "lot": "Lot C", "distance": 0.4},
        {"name": "Couch Center", "lot": "Lot D", "distance": 0.6},
        {"name": "Walker Center", "lot": "Lot E", "distance": 0.2},
        {"name": "Residential Colleges (Dunham & Headington College)", "lot": "Lot F", "distance": 0.7},
        {"name": "David L. Boren Hall", "lot": "Lot G", "distance": 0.5},
        {"name": "Headington Hall", "lot": "Lot H", "distance": 0.4},
        {"name": "Traditions Square", "lot": "Lot I", "distance": 0.6},
        {"name": "Kraettli Apartments", "lot": "Lot J", "distance": 0.3},
    ]

    for h in housing_list:
        Housing.objects.get_or_create(
            housingName=h["name"],
            closestParking=h["lot"],
            distance=h["distance"]
        )
