from django.shortcuts import render
from .services import getDashboardRows

def home(request):
    rows = getDashboardRows()

    # Fallback so the table is NEVER empty on your machine
    if not rows:
        rows = [
            {
                "building_name": "DEH",
                "lot_label": "S Jenkins & Page St, Norman, OK 73069",
                "available": None,
                "total": None,
            },
            {
                "building_name": "FH",
                "lot_label": "S Jenkins Ave & Page St, Norman, OK 73096",
                "available": None,
                "total": None,
            },
            {
                "building_name": "GH",
                "lot_label": "123 Example Rd, Norman, OK 73072",
                "available": None,
                "total": None,
            },
        ]
    return render(request, "datadashboard/home.html", {"rows": rows})

