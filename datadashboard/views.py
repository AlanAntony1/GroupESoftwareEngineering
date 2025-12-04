# datadashboard/views.py
from django.http import JsonResponse
from django.shortcuts import render
from parkingLotHistory.models import ParkingHistory

# Map buildings to lot codes + a readable lot label
PAIRS = [
    ("DEH", "LotA", "S Jenkins & Page St, Norman, OK 73069"),
    ("FH",  "LotB", "S Jenkins Ave & Page St, Norman, OK 73096"),
    ("GH",  "LotC", "123 Example Rd, Norman, OK 73072"),
]

def _dashboard_rows():
    rows = []
    for b_name, lot_code, lot_label in PAIRS:
        ph = (ParkingHistory.objects
              .filter(lot_name=lot_code)
              .order_by("-timestamp")
              .first())
        if ph:
            available = ph.available_spots
            total = ph.available_spots + ph.occupied_spots
        else:
            available = 0
            total = 0
        rows.append({
            "building_name": b_name,
            "lot_label": lot_label,
            "available": available,
            "total": total,
        })
    return rows

def home(request):
    # Render the HTML table
    return render(request, "datadashboard/home.html", {"rows": _dashboard_rows()})

def data_json(request):
    # Optional JSON endpoint for debugging
    return JsonResponse(_dashboard_rows(), safe=False)
