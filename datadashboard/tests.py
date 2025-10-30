from django.test import TestCase
from .models import ParkingLot

class ParkingLotModelTest(TestCase):
    def test_available_spaces_calculation(self):
        lot = ParkingLot.objects.create(
            name="Lot A",
            total_spaces=100,
            occupied_spaces=25
        )
        self.assertEqual(lot.available_spaces, 75)
        self.assertEqual(str(lot), "Lot A (75 free)")

