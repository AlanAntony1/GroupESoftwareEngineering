# datadashboard/views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Max, Count
from parkingLotHistory.models import ParkingHistory
from parkinglotlocater.models import Building

def _build_rows():
    """
    Build dashboard rows from the new schema:
      - building (from Building model)
      - lot_label (closest lot text from Building.closestLot)
      - last_seen (latest timestamp any user picked that building)
      - count (how many times this building was selected in history)

    NOTE: No available/total in the new schema, so we omit them.
    """
    # pre-aggregate usage from ParkingHistory by building_name
    agg = (
        ParkingHistory.objects
        .values("building_name")
        .annotate(last_seen=Max("timestamp"), count=Count("*"))
    )
    # turn into quick lookup dict
    stats_by_name = {a["building_name"]: a for a in agg}

    rows = []
    for b in Building.objects.all().order_by("buildingName"):
        stat = stats_by_name.get(b.buildingName, None)
        rows.append({
            "building":  b.buildingName,
            "lot_label": b.closestLot or "",
            "last_seen": (stat["last_seen"].isoformat() if stat and stat["last_seen"] else None),
            "count":     (stat["count"] if stat else 0),
        })
    return rows

def home(request):
    return render(request, "datadashboard/home.html", {"rows": _build_rows()})

def data_json(request):
    return JsonResponse(_build_rows(), safe=False)
