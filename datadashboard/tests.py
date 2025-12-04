# datadashboard/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from parkinglotlocater.models import Building
from parkingLotHistory.models import ParkingHistory

class DashboardPageTests(TestCase):
    def setUp(self):
        # Seed some buildings
        Building.objects.create(buildingName="DEH", closestLot="S Jenkins & Page St, Norman")
        Building.objects.create(buildingName="FH",  closestLot="S Jenkins Ave & Page St, Norman")
        Building.objects.create(buildingName="GH",  closestLot="123 Example Rd, Norman")

        # Seed some usage history tied to building_name (new schema)
        u = User.objects.create_user(username="test", password="x")
        now = timezone.now()
        ParkingHistory.objects.create(user=u, building_name="DEH", timestamp=now)
        ParkingHistory.objects.create(user=u, building_name="DEH", timestamp=now)
        ParkingHistory.objects.create(user=u, building_name="FH",  timestamp=now)

    def test_dashboard_home_renders(self):
        url = reverse("datadashboard:dashboard-home")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Data Dashboard")
        self.assertContains(resp, "Building")
        self.assertContains(resp, "Closest Lot")
        self.assertContains(resp, "Selections")

    def test_dashboard_data_json_shape(self):
        url = reverse("datadashboard:dashboard-data")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

        row = data[0]
        for key in ("building", "lot_label", "last_seen", "count"):
            self.assertIn(key, row)
        self.assertIsInstance(row["count"], int)
