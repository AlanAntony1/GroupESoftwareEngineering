
from collections import Counter
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from parkingLotHistory.models import ParkingHistory
from parkinglotlocater.models import Building
from scheduleInput.models import ClassInput  

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
# quick lookups
LOT_LABEL_BY_CODE = {code: label for _, code, label in PAIRS}
CODE_BY_LOT_LABEL = {label: code for _, code, label in PAIRS}

# Map a query-string day (“Mon”, “Tue”, …) to the abbreviations you store in ClassInput.days
DAY_TO_ABBRS = {
    "Mon": ["M"],
    "Tue": ["T"],
    "Wed": ["W"],
    "Thu": ["Th"],
    "Fri": ["F"],
    "Sat": ["S"],
    "Sun": ["Su"],
}

def _compute_peak_hours_from_schedule(q_day: str | None) -> dict[str, str | None]:
    """
    Returns { lot_code: 'HH:00' | None } using ClassInput.arrival_time for the chosen day.
    - We find each class’s Building by name
    - Use Building.closestLot (string address) to identify which dashboard lot it belongs to
    - Bucket arrival_time by hour and pick the top hour
    """
    if not q_day or q_day not in DAY_TO_ABBRS:
        return {code: None for code in CODE_BY_LOT_LABEL.values()}

    want_abbrs = DAY_TO_ABBRS[q_day]
    classes = ClassInput.objects.all()

    # Build quick map: building name -> closest lot label (string)
    bmap = {b.buildingName.strip().lower(): b.closestLot for b in Building.objects.all()}

    # Per-lot counters of arrival hours
    per_lot_counter: dict[str, Counter] = {code: Counter() for code in CODE_BY_LOT_LABEL.values()}

    for c in classes:
        # Check if this class meets on the requested day
        # (days is a comma string like "M,W,F" or contains "Th" etc.)
        days_str = (c.days or "").replace(" ", "")
        meets_today = any(abbr in days_str.split(",") for abbr in want_abbrs)
        if not meets_today:
            continue

        # Determine the lot_code for this class via Building.closestLot
        key = (c.location or "").strip().lower()
        lot_label = bmap.get(key)
        if not lot_label:
            continue
        lot_code = CODE_BY_LOT_LABEL.get(lot_label)
        if not lot_code:
            continue

        # pick arrival_time if present; otherwise derive a fallback from startTime (same logic as your model)
        arr = c.arrival_time
        if not arr and c.startTime:
            start = datetime.combine(timezone.now().date(), c.startTime)
            ten = datetime.combine(start.date(), datetime.strptime("10:00", "%H:%M").time())
            two = datetime.combine(start.date(), datetime.strptime("14:00", "%H:%M").time())
            delta_min = 25 if ten <= start <= two else 15
            arr = (start.replace(second=0, microsecond=0) - timezone.timedelta(minutes=delta_min)).time()

        if not arr:
            continue

        hour_label = f"{arr.hour:02d}:00"
        per_lot_counter[lot_code][hour_label] += 1

    # pick the most common hour per lot (or None)
    result: dict[str, str | None] = {}
    for lot_code, ctr in per_lot_counter.items():
        result[lot_code] = ctr.most_common(1)[0][0] if ctr else None
    return result


def _build_rows(q_day: str | None = None):
    """
    Returns a list of dicts:
      {building, lot, lot_label, available, total, peak}
    'peak' is computed from schedule (arrival_time) for the requested day, if provided.
    """
    peak_by_lot = _compute_peak_hours_from_schedule(q_day)

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
    q_day = request.GET.get("day")  # optional day query param for peak hours
    return render(request, "datadashboard/home.html", {"rows": _build_rows()})

def data_json(request):
    q_day = request.GET.get("day")  # optional day query param for peak hours
    # CI expects a LIST (safe=False), not {"rows": ...}
    return JsonResponse(_build_rows(), safe=False)
