from .models import Housing

def load_housing():
    housing_list = [
        "Cross Village",
        "McCasland Hall",
        "South Building",
        "Couch Center",
        "Walker Center",
        "Residential Colleges (Dunham & Headington College)",
        "David L. Boren Hall",
        "Headington Hall",
        "Traditions Square",
        "Kraettli Apartments",
    ]

    for name in housing_list:
        Housing.objects.get_or_create(name=name)
