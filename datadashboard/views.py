
# datadashboard/views.py
from django.http import JsonResponse
from django.shortcuts import render
from parkingLotHistory.models import ParkingHistory

# Building ↔ lot mapping (adjust as I like)
PAIRS = [
    ("Devon Energy Hall", "LotA", "S Jenkins Ave & Page St, Norman, OK 73069"),
    ("Felga Hall",  "LotB", "S Jenkins Ave & Page St, Norman, OK 73069"),
    ("Gallogly Hall",  "LotC", "S Jenkins Ave & Page St, Norman, OK 73069"),
    ("Sarkey's Energy Center", "LotD", "S Jenkins Ave & Page St, Norman, OK 73069"),
    ("Price College of Business", "LotE", "S Jenkins Ave, Norman, OK 73069"),
    ("Cater Hall", "LotF", "SW Lindsay Street and Asp Ave, Norman, OK 73069"),
    ("Dale Hall", "LotG", "SW 15th St & Asp Ave, Norman, OK 73069"),
    ("Nixon Library", "LotH", "SW 15th St & Asp Ave, Norman, OK 73069"),
    
]

def _build_rows():
    """
    Returns a list of dicts:
      {building, lot, lot_label, available, total}
    using the latest ParkingHistory per lot.
    """
    rows = []
    for building, lot_code, lot_label in PAIRS:
        ph = (
            ParkingHistory.objects
            .filter(lot_name=lot_code)
            .order_by("-timestamp")
            .first()
        )
        if ph:
            available = ph.available_spots
            total = ph.available_spots + ph.occupied_spots
        else:
            available = 0
            total = 0

        rows.append({
            "building":  building,
            "lot":       lot_code,   # tests expect the code like 'LotA'
            "lot_label": lot_label,  # optional for display
            "available": available,
            "total":     total,
        })
    return rows

def home(request):
    return render(request, "datadashboard/home.html", {"rows": _build_rows()})

def data_json(request):
    # CI expects a LIST (safe=False), not {"rows": ...}
    return JsonResponse(_build_rows(), safe=False)
