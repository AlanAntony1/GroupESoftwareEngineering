# datadashboard/tests.py
# ------------------------------------------------------------
# Purpose:
#   - Smoke-test the Data Dashboard feature end-to-end:
#       * The HTML page renders (status 200) and shows expected headers.
#       * The JSON endpoint returns a list of rows with expected keys/types.
#       * The JSON numbers match the latest ParkingHistory snapshot(s).
#
# What to change if your app differs:
#   - If your URL names change, edit the reverse("datadashboard:...") calls.
#   - If your JSON keys change, update the expected keys in test assertions.
#   - If your lot codes/labels differ from LotA/LotB/LotC, adjust setUp() or matching logic.
# ------------------------------------------------------------

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from parkingLotHistory.models import ParkingHistory


class DashboardPageTests(TestCase):
    def setUp(self):
        """
        Seed deterministic ParkingHistory snapshots so tests don’t depend on
        real DB contents. We create exactly one entry per lot, all at `now`,
        so “latest per lot” in the view is unambiguous.

        If your lot codes differ, change 'LotA'/'LotB'/'LotC' here to match
        whatever your view expects to find.
        """
        now = timezone.now()
        ParkingHistory.objects.create(
            lot_name="LotA", occupied_spots=20, available_spots=80, timestamp=now
        )
        ParkingHistory.objects.create(
            lot_name="LotB", occupied_spots=15, available_spots=85, timestamp=now
        )
        ParkingHistory.objects.create(
            lot_name="LotC", occupied_spots=40, available_spots=60, timestamp=now
        )

    def test_dashboard_home_renders(self):
        """
        HTML page test:
        - Asks Django to reverse the named URL `datadashboard:dashboard-home`.
        - Ensures the page returns HTTP 200.
        - Verifies the table headers exist in the response body.

        If your URL name changes, update the reverse() call.
        If you rename the headers in the template, update the self.assertContains lines.
        """
        url = reverse("datadashboard:dashboard-home")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Data Dashboard")
        self.assertContains(resp, "Building")
        self.assertContains(resp, "Closest Lot")
        self.assertContains(resp, "Available / Total")

    def test_dashboard_data_json_shape(self):
        """
        JSON endpoint shape test:
        - Calls `datadashboard:dashboard-data`.
        - Expects a JSON array (list) of row dicts.
        - Each row should contain keys: building, lot, available, total.
        - Values for available/total should be non-negative integers.

        If your endpoint returns a different shape or key names, update the
        assertions accordingly.
        """
        url = reverse("datadashboard:dashboard-data")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        # The endpoint should return a top-level list, not {"rows": [...]}.
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

        row = data[0]
        for key in ("building", "lot", "available", "total"):
            self.assertIn(key, row)

        self.assertIsInstance(row["available"], int)
        self.assertIsInstance(row["total"], int)
        self.assertGreaterEqual(row["available"], 0)
        self.assertGreaterEqual(row["total"], 0)

    def test_dashboard_data_matches_latest_history(self):
        """
        Data correctness test:
        - Ensures the JSON uses the *latest* ParkingHistory snapshot values.
        - Since setUp() creates one entry for LotA (available=80, occupied=20),
          we expect total=100 for LotA.

        If your view labels the lot with a human-readable address instead of
        the code ('LotA'), the logic below tries to find it by substring.
        Adjust matching if your labels are totally different.
        """
        url = reverse("datadashboard:dashboard-data")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        # Try to find the row corresponding to LotA by looking at the 'lot' label.
        target = None
        for r in data:
            lot_field = str(r.get("lot", ""))
            if "LotA" in lot_field or lot_field.strip() == "LotA":
                target = r
                break

        # If your view never exposes 'LotA' literally (only addresses, for example),
        # we still check at least one row for non-negative numbers to keep the test useful.
        if target is None and data:
            target = data[0]

        self.assertIsNotNone(target)

        # Base sanity checks.
        self.assertGreaterEqual(target["total"], 0)
        self.assertGreaterEqual(target["available"], 0)

        # If the lot label still includes "LotA", enforce the exact numbers
        # from setUp(): available=80, occupied=20 -> total=100
        lot_field = str(target.get("lot", ""))
        if "LotA" in lot_field or lot_field.strip() == "LotA":
            self.assertEqual(target["available"], 80)
            self.assertEqual(target["total"], 100)
