# datadashboard/services.py
from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Dict, Optional
import json

from parkingLotHistory.models import ParkingHistory


@dataclass(frozen=True)
class DateRange:
    start: date
    end: date


def getDashboardRows() -> List[Dict]:
    """
    Returns rows like:
      {"building_name": ..., "lot_label": ..., "available": ..., "total": ...}
    Uses the latest ParkingHistory per lot.
    """
    pairs = [
        ("DEH", "LotA", "S Jenkins & Page St, Norman, OK 73069"),
        ("FH",  "LotB", "S Jenkins Ave & Page St, Norman, OK 73096"),
        ("GH",  "LotC", "123 Example Rd, Norman, OK 73072"),
    ]

    rows: List[Dict] = []
    for building_name, lot_code, lot_label in pairs:
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
            available = None
            total = None

        rows.append({
            "building_name": building_name,
            "lot_label": lot_label,
            "available": available,
            "total": total,
        })
    return rows


def _validate_daterange(dr: DateRange):
    if not isinstance(dr, DateRange):
        raise TypeError("dateRange must be a DateRange object")
    if dr.start is None or dr.end is None:
        raise ValueError("dateRange requires both start and end")
    if dr.start > dr.end:
        raise ValueError("start date cannot be after end date")


def getUsageStats(dateRange: DateRange) -> List[Dict]:
    """Return total occupied/available spots per day (inclusive range)."""
    _validate_daterange(dateRange)
    results: List[Dict] = []
    current = dateRange.start
    while current <= dateRange.end:
        qs = ParkingHistory.objects.filter(timestamp__date=current)
        if qs.exists():
            occupied = sum(x.occupied_spots for x in qs)
            available = sum(x.available_spots for x in qs)
            results.append({"date": current, "occupied": occupied, "available": available})
        current += timedelta(days=1)
    return results


def getPeakHours(lotId: str) -> Optional[Dict]:
    """Return the hour with the highest occupancy for the given lot."""
    if not isinstance(lotId, str) or not lotId.strip():
        raise TypeError("lotId must be a non-empty string")

    entries = ParkingHistory.objects.filter(lot_name=lotId).order_by("timestamp")
    if not entries.exists():
        return None

    hourly = {}
    for e in entries:
        hr = e.timestamp.replace(minute=0, second=0, microsecond=0)
        hourly[hr] = hourly.get(hr, 0) + e.occupied_spots

    peak_hour = max(hourly, key=hourly.get)
    return {"hour": peak_hour, "occupied": hourly[peak_hour]}


def exportAnalytics(fmt: str, dateRange: Optional[DateRange] = None) -> str:
    """Export stats as CSV or JSON."""
    if dateRange is None:
        today = date.today()
        dateRange = DateRange(today, today)

    stats = getUsageStats(dateRange)
    f = (fmt or "").lower()

    if f == "json":
        return json.dumps(stats, default=str)
    if f == "csv":
        lines = ["date,occupied,available"]
        for s in stats:
            lines.append(f"{s['date']},{s['occupied']},{s['available']}")
        return "\n".join(lines)
    raise ValueError("Unsupported format; use 'csv' or 'json'")
