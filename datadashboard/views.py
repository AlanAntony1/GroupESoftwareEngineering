
# datadashboard/views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Max
from parkingLotHistory.models import ParkingHistory

# Optional mapping: show friendly building/lot labels
LOT_TO_BUILDING = {
    "LotA": "DEH",
    "LotB": "FH",
    "LotC": "GH",
}
LOT_LABELS = {
    "LotA": "S Jenkins & Page St, Norman",
    "LotB": "S Jenkins Ave & Page St, Norman",
    "LotC": "123 Example Rd, Norman",
}

def _fetch_rows():
    """
    Build rows from the latest ParkingHistory for each lot_name.
    Row keys match the template: building, lot, available, total.
    """
    # Find the latest timestamp for each lot_name
    latest = (
        ParkingHistory.objects
        .values("lot_name")
        .annotate(last_ts=Max("timestamp"))
    )

    rows = []
    for item in latest:
        ph = (ParkingHistory.objects
              .filter(lot_name=item["lot_name"], timestamp=item["last_ts"])
              .first())
        if not ph:
            continue
        total = (ph.occupied_spots or 0) + (ph.available_spots or 0)
        rows.append({
            "building": LOT_TO_BUILDING.get(ph.lot_name, ph.lot_name),
            "lot":      LOT_LABELS.get(ph.lot_name, ph.lot_name),
            "available": ph.available_spots or 0,
            "total":     total,
        })
    return rows

def home(request):
    rows = _fetch_rows()
    return render(request, "datadashboard/home.html", {"rows": rows})

def data_json(request):
    return JsonResponse({"rows": _fetch_rows()})

def ping(request):
    return JsonResponse({"ok": True, "view": "datadashboard"})
