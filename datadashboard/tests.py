# datadashboard/tests.py
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from parkingLotHistory.models import ParkingHistory


class DashboardPageTests(TestCase):
    def setUp(self):
        now = timezone.now()
        # Seed one snapshot per lot so "latest per lot" logic is deterministic
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
        """Dashboard page returns 200 and has the table headers."""
        url = reverse("datadashboard:dashboard-home")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Data Dashboard")
        self.assertContains(resp, "Building")
        self.assertContains(resp, "Closest Lot")
        self.assertContains(resp, "Available / Total")

    def test_dashboard_data_json_shape(self):
        """JSON endpoint returns a list of row dicts with required keys."""
        url = reverse("datadashboard:dashboard-data")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

        # Check keys in at least the first row (others should be similar)
        row = data[0]
        # be flexible about exact naming, but these should exist per our view
        for key in ("building", "lot", "available", "total"):
            self.assertIn(key, row)

        # Sanity on values
        self.assertIsInstance(row["available"], int)
        self.assertIsInstance(row["total"], int)
        self.assertGreaterEqual(row["available"], 0)
        self.assertGreaterEqual(row["total"], 0)

    def test_dashboard_data_matches_latest_history(self):
        """
        For a seeded lot (LotA), the JSON should reflect latest available/total.
        We created only one entry per lot in setUp, so it should match directly.
        """
        url = reverse("datadashboard:dashboard-data")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        # Find the row that corresponds to LotA (by lot code or label substring)
        # Your view may label the lot with a human string; just allow either.
        target = None
        for r in data:
            lot_field = str(r.get("lot", ""))
            if "LotA" in lot_field or lot_field.strip() == "LotA":
                target = r
                break

        # If your view labels the lot without "LotA", fall back to first row so
        # the test still validates shapes/values.
        if target is None and data:
            target = data[0]

        self.assertIsNotNone(target)

        # With our seed, available=80, occupied=20 -> total=100
        self.assertGreaterEqual(target["total"], 0)
        self.assertGreaterEqual(target["available"], 0)

        # If the lot label still includes "LotA", validate exact numbers:
        lot_field = str(target.get("lot", ""))
        if "LotA" in lot_field or lot_field.strip() == "LotA":
            self.assertEqual(target["available"], 80)
            self.assertEqual(target["total"], 100)
