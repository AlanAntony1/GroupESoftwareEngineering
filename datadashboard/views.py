
from django.http import JsonResponse
from django.shortcuts import render
from parkingLotHistory.models import ParkingHistory

# Building -> (Lot Code, Human label)
PAIRS = [
    ("DEH", "LotA", "S Jenkins & Page St, Norman"),
    ("FH",  "LotB", "S Jenkins Ave & Page St, Norman"),
    ("GH",  "LotC", "123 Example Rd, Norman"),
]

def _build_rows():
    rows = []
    for building, lot_code, lot_label in PAIRS:
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
            "building":   building,
            "lot":        lot_code,   # <-- IMPORTANT: lot is the CODE for tests
            "lot_label":  lot_label,  # (optional) keep label for your template
            "available":  available,
            "total":      total,
        })
    return rows

def home(request):
    rows = _build_rows()
    return render(request, "datadashboard/home.html", {"rows": rows})

def dashboard_data(request):
    # <-- IMPORTANT: return a bare list, not {"rows": [...]}
    return JsonResponse(_build_rows(), safe=False)
