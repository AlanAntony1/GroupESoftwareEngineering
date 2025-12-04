
# datadashboard/views.py
# ------------------------------------------------------------
# Purpose:
#   Serve the Data Dashboard page (HTML) and a JSON feed used by tests/clients.
#   The data is built from the latest ParkingHistory snapshot for a few
#   pre-mapped campus buildings.
#
# What to change:
#   - To add/remove buildings or change the human label shown in the table,
#     edit the PAIRS list below.
#   - If you want different keys in the JSON (e.g., add "lot_code"), change
#     the dict built in _build_rows().
#   - If you want to show a different “latest” rule (e.g., last 24h only),
#     update the ParkingHistory query in _build_rows().
#
# Test expectations (important):
#   - The JSON endpoint at name "datadashboard:dashboard-data" must return a
#     TOP-LEVEL LIST of dicts (NOT {"rows": [...]}), so we use JsonResponse(..., safe=False).
#   - Each row dict should include: "building", "lot", "available", "total".
#     (We also include "lot_label" for display; tests ignore it.)
# ------------------------------------------------------------

from django.http import JsonResponse
from django.shortcuts import render
from parkingLotHistory.models import ParkingHistory

# Building ↔ lot mapping used by the dashboard.
# Format: (building_code, lot_code_in_DB, human_readable_lot_label)
# - building_code: short string you want to display in the "Building" column
# - lot_code_in_DB: must match ParkingHistory.lot_name values (e.g., "LotA")
# - human_readable_lot_label: pretty text for the UI table (optional)
PAIRS = [
    ("DEH", "LotA", "S Jenkins & Page St, Norman"),
    ("FH",  "LotB", "S Jenkins Ave & Page St, Norman"),
    ("GH",  "LotC", "123 Example Rd, Norman"),
]

def _build_rows():
    """
    Build the dashboard rows from latest ParkingHistory per lot in PAIRS.

    Returns: list[dict] with keys:
      - building:   the campus building code (e.g., "DEH")
      - lot:        the lot code (e.g., "LotA") — tests look for this
      - lot_label:  human label for display ("S Jenkins & Page St, Norman")
      - available:  integer, available spots for the latest snapshot
      - total:      integer, available + occupied (0 if no snapshot)
    """
    rows = []

    for building, lot_code, lot_label in PAIRS:
        # Grab the MOST RECENT snapshot for this lot_code.
        # If you want a time filter (e.g., only today), add a .filter(timestamp__date=...)
        ph = (
            ParkingHistory.objects
            .filter(lot_name=lot_code)
            .order_by("-timestamp")
            .first()
        )

        if ph:
            # Latest numbers from the snapshot
            available = ph.available_spots
            total = ph.available_spots + ph.occupied_spots
        else:
            # If there is no data in the DB yet for this lot, show zeros
            available = 0
            total = 0

        rows.append({
            "building":  building,
            "lot":       lot_code,   # tests expect a "lot" field with the code like 'LotA'
            "lot_label": lot_label,  # optional: used only for nicer display in the HTML
            "available": available,
            "total":     total,
        })

    return rows

def home(request):
    """
    Render the HTML page (template: datadashboard/home.html).
    The template expects 'rows' in the context to build the table.
    """
    return render(request, "datadashboard/home.html", {"rows": _build_rows()})

def data_json(request):
    """
    JSON API endpoint used by tests and (optionally) the UI.

    NOTE: We return a top-level LIST, not an object, because tests call:
          data = resp.json(); assert isinstance(data, list)
    That’s why we pass safe=False to JsonResponse.
    """
    return JsonResponse(_build_rows(), safe=False)
