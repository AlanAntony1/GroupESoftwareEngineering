
# datadashboard/views.py
from django.http import JsonResponse
from django.shortcuts import render

from parkingLotHistory.models import ParkingHistory
from parkinglotlocater.models import Building  # ← pull data from locator app

# If ParkingHistory.lot_name uses short codes (e.g., "LotA")
# but the locator stores human labels (e.g., "S Jenkins & Page St, Norman"),
# map them here. If your PH.lot_name ALREADY stores the same human label,
# you can leave this dict empty.
LOT_LABEL_TO_CODE = {
    # "S Jenkins & Page St, Norman": "LotA",
    # "S Jenkins Ave & Page St, Norman": "LotB",
    # "123 Example Rd, Norman": "LotC",
}

def _lot_code_from_label(label: str) -> str:
    if not label:
        return ""
    return LOT_LABEL_TO_CODE.get(label, label)  # fall back to the label itself

def _build_rows():
    """
    Create table rows from Buildings in the locator app.
    Each row shape matches your template:
      {building, lot, lot_label, available, total}
    """
    rows = []

    for b in Building.objects.all().order_by("buildingName"):
        building_name = getattr(b, "buildingName", "")
        lot_label = getattr(b, "closestLot", "") or ""
        lot_code = _lot_code_from_label(lot_label)

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
            "building":  building_name,
            "lot":       lot_code,     # useful in tests
            "lot_label": lot_label,    # what the table displays
            "available": available,
            "total":     total,
        })

    return rows

def home(request):
    return render(request, "datadashboard/home.html", {"rows": _build_rows()})

def data_json(request):
    # Tests and the API expect a LIST, not {"rows": ...}
    return JsonResponse(_build_rows(), safe=False)
