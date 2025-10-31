# datadashboard/services.py
from dataclasses import dataclass
from datetime import date, timedelta
import json
from typing import List, Dict, Optional
from parkingLotHistory.models import ParkingHistory


@dataclass(frozen=True)
class DateRange:
    start: date
    end: date


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

    results = []
    current = dateRange.start
    while current <= dateRange.end:
        daily = ParkingHistory.objects.filter(timestamp__date=current)
        occupied = sum(x.occupied_spots for x in daily)
        available = sum(x.available_spots for x in daily)
        if daily.exists():
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

    # Group manually by hour (simple loop)
    hourly = {}
    for e in entries:
        hr = e.timestamp.replace(minute=0, second=0, microsecond=0)
        hourly[hr] = hourly.get(hr, 0) + e.occupied_spots

    peak_hour = max(hourly, key=hourly.get)
    return {"hour": peak_hour, "occupied": hourly[peak_hour]}


def exportAnalytics(format: str, dateRange: Optional[DateRange] = None) -> str:
    """Export stats as CSV or JSON."""
    today = date.today()
    if dateRange is None:
        dateRange = DateRange(today, today)
    stats = getUsageStats(dateRange)
    fmt = (format or "").lower()
    if fmt == "json":
        return json.dumps(stats, default=str)
    elif fmt == "csv":
        text = "date,occupied,available\n"
        for s in stats:
            text += f"{s['date']},{s['occupied']},{s['available']}\n"
        return text
    else:
        raise ValueError("Unsupported format; use 'csv' or 'json'")
