from django.test import TestCase

# Create your tests here.
from .models import AvailableLots

class AvailableLotsTestCase(TestCase):
    def setUp(self):
        self.lot = AvailableLots.objects.create(
            lot_name="OU South Garage",
            total_spaces=100,
            available_spaces=60
        )

    def test_initial_status(self):
        self.assertEqual(self.lot.status, "Open")

    def test_update_availability_to_full(self):
        self.lot.update_availability(0)
        self.assertEqual(self.lot.status, "Full")

    def test_occupancy_rate(self):
        rate = self.lot.occupancy_rate()
        self.assertEqual(rate, 40.0)