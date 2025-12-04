
# datadashboard/views.py
from django.http import JsonResponse
from django.shortcuts import render
from parkingLotHistory.models import ParkingHistory

# Building ↔ lot mapping (adjust as you like)
PAIRS = [
    ("DEH", "LotA", "S Jenkins & Page St, Norman"),
    ("FH",  "LotB", "S Jenkins Ave & Page St, Norman"),
    ("GH",  "LotC", "123 Example Rd, Norman"),
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
