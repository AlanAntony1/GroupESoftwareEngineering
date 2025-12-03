# datadashboard/tests.py
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone

from parkingLotHistory.models import ParkingHistory
from datadashboard.services import DateRange, getUsageStats, getPeakHours, exportAnalytics


class SimpleDashboardTests(TestCase):
    def setUp(self):
        today = timezone.localdate()
        now = timezone.now()

        # Two simple entries for today
        ParkingHistory.objects.create(
            lot_name="LotA", occupied_spots=10, available_spots=90, timestamp=now
        )
        ParkingHistory.objects.create(
            lot_name="LotA", occupied_spots=20, available_spots=80, timestamp=now
        )

        # One entry for yesterday (safe across month boundaries)
        yesterday = today - timedelta(days=1)
        ParkingHistory.objects.create(
            lot_name="LotB",
            occupied_spots=5,
            available_spots=95,
            timestamp=now - timedelta(days=1),
        )


    def test_getUsageStats(self):
        """Check that usage stats return at least one record"""
        today = timezone.localdate()
        dr = DateRange(today, today)
        stats = getUsageStats(dr)
        self.assertIsInstance(stats, list)
        self.assertGreater(len(stats), 0)

    def test_getPeakHours(self):
        """Peak hour should exist for LotA"""
        res = getPeakHours("LotA")
        self.assertIsNotNone(res)
        self.assertIn("occupied", res)

    def test_getPeakHours_empty(self):
        """Nonexistent lot returns None"""
        self.assertIsNone(getPeakHours("NoLot"))

    def test_exportAnalytics_csv(self):
        """Export CSV output contains header"""
        today = timezone.localdate()
        dr = DateRange(today, today)
        csv_text = exportAnalytics("csv", dr)
        self.assertTrue(csv_text.startswith("date,occupied,available"))

    def test_exportAnalytics_json(self):
        """Export JSON output is valid"""
        today = timezone.localdate()
        dr = DateRange(today, today)
        text = exportAnalytics("json", dr)
        # It should contain at least the word 'occupied'
        self.assertIn("occupied", text)
