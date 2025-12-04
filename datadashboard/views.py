
# datadashboard/views.py
from django.http import JsonResponse
from django.shortcuts import render
from parkingLotHistory.models import ParkingHistory
from django.db.models import Sum
from django.db.models.functions import ExtractHour, ExtractWeekDay
from datetime import timedelta

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
# --- PEAK HOUR (typical) -----------------------------------------------------
# We’ll compute "typical" as: for each weekday, which hour has the highest
# *average* occupied spots over the last N days (default 60).

# Reuse the same lot list you used in _build_rows()
_LOT_PAIRS = [
    ("DEH", "LotA", "S Jenkins & Page St, Norman"),
    ("FH",  "LotB", "S Jenkins Ave & Page St, Norman"),
    ("GH",  "LotC", "123 Example Rd, Norman"),
]
_LOT_CODES = [c for _, c, _ in _LOT_PAIRS]

def typical_peaks_for_lot(lot_code: str, window_days: int = 60):
    """
    Return a dict:
      {
        "lot": "LotA",
        "window_days": 60,
        "by_weekday": [
           {"weekday": 1, "hour": 14, "avg_occupied": 37},
           ... one row per weekday 1..7 ...
        ],
        "overall": {"hour": 14, "avg_occupied": 42}
      }
    Weekday is 1=Sun … 7=Sat (Django's ExtractWeekDay).
    """
    if lot_code not in _LOT_CODES:
        return {"lot": lot_code, "window_days": window_days, "by_weekday": [], "overall": None}

    since = timezone.now() - timedelta(days=window_days)

    # 1) Aggregate occupancy by (weekday, hour)
    qs = (
        ParkingHistory.objects
        .filter(lot_name=lot_code, timestamp__gte=since)
        .annotate(weekday=ExtractWeekDay("timestamp"), hour=ExtractHour("timestamp"))
        .values("weekday", "hour")
        .annotate(occ=Sum("occupied_spots"))
    )

    # Build a dict {(weekday, hour) -> occ}
    grid = {}
    for r in qs:
        grid[(int(r["weekday"]), int(r["hour"]))] = int(r["occ"])

    # 2) For each weekday, pick the hour with max occupied
    by_weekday = []
    for wd in range(1, 8):  # 1..7
        best_hour, best_occ = None, -1
        for hr in range(0, 24):
            occ = grid.get((wd, hr), 0)
            if occ > best_occ:
                best_occ = occ
                best_hour = hr
        if best_hour is not None:
            by_weekday.append({"weekday": wd, "hour": best_hour, "avg_occupied": best_occ})

    # 3) Overall typical hour across all weekdays
    overall_hour, overall_occ = None, -1
    # Sum across weekdays by hour
    hourly_total = {hr: 0 for hr in range(24)}
    for wd in range(1, 8):
        for hr in range(24):
            hourly_total[hr] += grid.get((wd, hr), 0)
    for hr, total in hourly_total.items():
        if total > overall_occ:
            overall_occ, overall_hour = total, hr

    return {
        "lot": lot_code,
        "window_days": window_days,
        "by_weekday": by_weekday,
        "overall": {"hour": overall_hour, "avg_occupied": overall_occ} if overall_hour is not None else None,
    }

def home(request):
    rows = _build_rows()

    # Compute typical peaks for the lots we show (last 60 days)
    peaks = {lot: typical_peaks_for_lot(lot, window_days=60) for lot in _LOT_CODES}

    return render(
        request,
        "datadashboard/home.html",
        {
            "rows": rows,
            "peaks": peaks,   # <-- add this
        },
    )


def data_json(request):
    # CI expects a LIST (safe=False), not {"rows": ...}
    return JsonResponse(_build_rows(), safe=False)
