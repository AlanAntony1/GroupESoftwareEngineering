import csv
from dataclasses import dataclass
from datetime import time
from typing import List, Dict, Any

from availableLots.models import AvailableLots


# Data structure for schedule items
""" This is only for example, no data is accurate to the university. Lots are
represented with simple coordinates for distance calculation. This is data that is not 
sourced from the database."""
@dataclass
class ScheduleItem:
    course: str
    building: str
    day_of_week: str
    start_time: time
    end_time: time
    pass_type: str


# Static data for buildings and lots (example purposes only)
# Buildings
BUILDING_COORDS = {
    "DEV": (0, 0),
    "PHSC": (2, 1),
    "NIELSEN": (-1, 3),
    "DAH": (1, 2),            # Dale Hall
    "GOULD": (3, -1),         # Gould Hall
}

LOT_COORDS = {
    "Asp Avenue Parking Facility": (1, -1),  
    "Elm Avenue Parking Facility": (3, 0),   
    "Jenkins Garage": (0, 1),               
}

LOT_PASS_TYPES = {
    "Asp Avenue Parking Facility": {"COMMUTER", "FACULTY", "STAFF"},
    "Elm Avenue Parking Facility": {"COMMUTER", "FACULTY", "STAFF"},
    "Jenkins Garage": {"COMMUTER", "FACULTY"},
}



# ----------------- Helper functions -----------------
def parse_time(hhmm: str) -> time:
    hh, mm = hhmm.split(":")
    return time(hour=int(hh), minute=int(mm))


def parse_schedule_csv(file_obj) -> List[ScheduleItem]:
    decoded = file_obj.read().decode("utf-8").splitlines()
    reader = csv.DictReader(decoded)

    items = []
    for row in reader:
        items.append(
            ScheduleItem(
                course=row["course"],
                building=row["building"],
                day_of_week=row["day_of_week"],
                start_time=parse_time(row["start_time"]),
                end_time=parse_time(row["end_time"]),
                pass_type=row["pass_type"],
            )
        )
    return items


def walking_distance(building: str, lot_name: str) -> float:
    bx, by = BUILDING_COORDS[building]
    lx, ly = LOT_COORDS[lot_name]
    return ((bx - lx) ** 2 + (by - ly) ** 2) ** 0.5


def score_lot(item: ScheduleItem, lot: AvailableLots) -> float:
    # Restrict by pass type
    allowed = LOT_PASS_TYPES.get(lot.lot_name, set())
    if item.pass_type not in allowed:
        return 1e9

    dist = walking_distance(item.building, lot.lot_name)
    occupancy = lot.occupancy_rate()

    # Prime location bonus for Asp Avenue
    asp_bonus = -0.15 if lot.lot_name == "Asp Avenue Parking Facility" else 0

    # Lower = better
    score = (dist * 1.0) + (occupancy / 100) * 0.7 + asp_bonus
    return score

def recommend_lot(item: ScheduleItem) -> str:
    lots = [lot for lot in AvailableLots.objects.all()
            if lot.lot_name in LOT_COORDS]

    best_lot = None
    best_score = float("inf")

    for lot in lots:
        s = score_lot(item, lot)
        if s < best_score:
            best_score = s
            best_lot = lot

    return best_lot.lot_name if best_lot else ""


def recommend_for_schedule(items: List[ScheduleItem]) -> List[Dict[str, Any]]:
    results = []
    for item in items:
        recommended = recommend_lot(item)
        results.append(
            {
                "course": item.course,
                "building": item.building,
                "recommended_lot": recommended,
            }
        )
    return results
