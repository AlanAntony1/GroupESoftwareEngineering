
# datadashboard/views.py
from collections import Counter
from datetime import datetime, timedelta
from typing import Dict, Optional

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from parkingLotHistory.models import ParkingHistory
from parkinglotlocater.models import Building
from scheduleInput.models import ClassInput

# Building ↔ lot mapping (make sure building spellings match your data)
PAIRS = [
    ("Devon Energy Hall",         "LotA", "S Jenkins Ave & Page St, Norman, OK 73069"),
    ("Felgar Hall",               "LotB", "S Jenkins Ave & Page St, Norman, OK 73069"),
    ("Gallogly Hall",             "LotC", "S Jenkins Ave & Page St, Norman, OK 73069"),
    ("Sarkeys Energy Center",     "LotD", "S Jenkins Ave & Page St, Norman, OK 73069"),
    ("Price College of Business", "LotE", "S Jenkins Ave, Norman, OK 73069"),
    ("Cate Center Dining Hall",   "LotF", "SW Lindsay Street and Asp Ave, Norman, OK 73069"),
    ("Dale Hall",                 "LotG", "SW 15th St & Asp Ave, Norman, OK 73069"),
    ("Nielsen Hall",              "LotH", "SW 15th St & Asp Ave, Norman, OK 73069"),
]

# quick lookups
LOT_LABEL_BY_CODE = {code: label for _, code, label in PAIRS}
CODE_BY_LOT_LABEL = {label: code for _, code, label in PAIRS}

# Map a query-string day (“Mon”, “Tue”, …) to the abbreviations you store in ClassInput.days
DAY_TO_ABBRS: Dict[str, list[str]] = {
    "Mon": ["M"],
    "Tue": ["T"],
    "Wed": ["W"],
    "Thu": ["Th"],
    "Fri": ["F"],
    "Sat": ["S"],
    "Sun": ["Su"],
}

def _latest_history_for(building: str, lot_code: str, lot_label: str) -> Optional[ParkingHistory]:
    """
    Return the latest ParkingHistory row using whatever columns exist.
    Tries (in order): lot_name, closest_lot, building_name.
    (This makes it work both on CI and your live server.)
    """
    Model = ParkingHistory
    fields = {f.name for f in Model._meta.get_fields()}

    if "lot_name" in fields:
        qs = Model.objects.filter(lot_name=lot_code)
    elif "closest_lot" in fields:
        qs = Model.objects.filter(closest_lot=lot_label)
    elif "building_name" in fields:
        qs = Model.objects.filter(building_name=building)
    else:
        return None

    return qs.order_by("-timestamp").first()

def _compute_peak_hours_from_schedule(q_day: Optional[str]) -> Dict[str, Optional[str]]:
    """
    Returns { lot_code: 'HH:00' | None } using ClassInput.arrival_time for the chosen day.
    We:
      - find Building by name
      - use its closestLot to map to your dashboard lot
      - bucket by arrival hour and pick the most common
    """
    if not q_day or q_day not in DAY_TO_ABBRS:
        return {code: None for code in CODE_BY_LOT_LABEL.values()}

    want_abbrs = DAY_TO_ABBRS[q_day]
    classes = ClassInput.objects.all()

    # building name -> closest lot label (string)
    bmap = {b.buildingName.strip().lower(): b.closestLot for b in Building.objects.all()}

    per_lot_counter: Dict[str, Counter] = {code: Counter() for code in CODE_BY_LOT_LABEL.values()}

    for c in classes:
        # days stored like "M,W,F" etc.
        days_str = (c.days or "").replace(" ", "")
        meets_today = any(abbr in days_str.split(",") for abbr in want_abbrs)
        if not meets_today:
            continue

        # map class location -> building -> closest lot -> lot code
        key = (c.location or "").strip().lower()
        lot_label = bmap.get(key)
        if not lot_label:
            continue
        lot_code = CODE_BY_LOT_LABEL.get(lot_label)
        if not lot_code:
            continue

        # choose arrival_time if present; else derive from startTime (same logic as your model)
        arr = c.arrival_time
        if not arr and c.startTime:
            start = datetime.combine(timezone.now().date(), c.startTime)
            ten = datetime.combine(start.date(), datetime.strptime("10:00", "%H:%M").time())
            two = datetime.combine(start.date(), datetime.strptime("14:00", "%H:%M").time())
            delta_min = 25 if ten <= start <= two else 15
            arr = (start.replace(second=0, microsecond=0) - timedelta(minutes=delta_min)).time()

        if not arr:
            continue

        hour_label = f"{arr.hour:02d}:00"
        per_lot_counter[lot_code][hour_label] += 1

    result: Dict[str, Optional[str]] = {}
    for lot_code, ctr in per_lot_counter.items():
        result[lot_code] = ctr.most_common(1)[0][0] if ctr else None
    return result

def _build_rows(q_day: Optional[str] = None):
    """
    Returns list of dicts:
      {building, lot, lot_label, available, total, peak}
    - availability comes from latest ParkingHistory (if fields exist)
    - peak comes from scheduleInput for the requested day (optional)
    """
    peak_by_lot = _compute_peak_hours_from_schedule(q_day)

    rows = []
    for building, lot_code, lot_label in PAIRS:
        ph = _latest_history_for(building, lot_code, lot_label)

        available = None
        total = None
        if ph is not None and hasattr(ph, "available_spots") and hasattr(ph, "occupied_spots"):
            available = int(ph.available_spots or 0)
            total = int((ph.available_spots or 0) + (ph.occupied_spots or 0))

        rows.append({
            "building":  building,
            "lot":       lot_code,
            "lot_label": lot_label,
            "available": available,      # may be None on live data until you store counts
            "total":     total,          # may be None on live data
            "peak":      peak_by_lot.get(lot_code),
        })
    return rows

def home(request):
    q_day = request.GET.get("day")  # e.g. /dashboard/?day=Mon
    return render(request, "datadashboard/home.html", {"rows": _build_rows(q_day)})

def data_json(request):
    q_day = request.GET.get("day")
    return JsonResponse(_build_rows(q_day), safe=False)
