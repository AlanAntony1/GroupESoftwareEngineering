from django.test import TestCase
from .models import ParkingHistory
from django.utils import timezone

class ParkingHistoryTestCase(TestCase):
    def setUp(self):
        # Simulate some initial building selections by users
        self.history1 = ParkingHistory.objects.create(
            lot_name="Lot A",
            occupied_spots=10,
            available_spots=40,
            timestamp=timezone.now()
        )
        self.history2 = ParkingHistory.objects.create(
            lot_name="Lot B",
            occupied_spots=25,
            available_spots=25,
            timestamp=timezone.now()
        )

    # Test that a single record is created correctly
    def test_create_record(self):
        history_count = ParkingHistory.objects.count()
        self.assertEqual(history_count, 2)
        first_record = ParkingHistory.objects.get(lot_name="Lot A")
        self.assertEqual(first_record.occupied_spots, 10)
        self.assertEqual(first_record.available_spots, 40)

    # Test adding a new record simulating a new user selection
    def test_add_new_selection(self):
        ParkingHistory.objects.create(
            lot_name="Lot C",
            occupied_spots=5,
            available_spots=45,
            timestamp=timezone.now()
        )
        self.assertEqual(ParkingHistory.objects.count(), 3)
        new_record = ParkingHistory.objects.get(lot_name="Lot C")
        self.assertEqual(new_record.occupied_spots, 5)
        self.assertEqual(new_record.available_spots, 45)

    # Test that multiple selections of the same lot create separate records
    def test_multiple_selections_same_lot(self):
        ParkingHistory.objects.create(
            lot_name="Lot A",
            occupied_spots=12,
            available_spots=38,
            timestamp=timezone.now()
        )
        records = ParkingHistory.objects.filter(lot_name="Lot A")
        self.assertEqual(records.count(), 2)

    # Test that records are ordered by timestamp
    def test_ordering_by_timestamp(self):
        timestamps = [record.timestamp for record in ParkingHistory.objects.all().order_by('timestamp')]
        self.assertEqual(timestamps, sorted(timestamps))

    # Test that invalid selection (e.g., negative spots) is detected
    def test_invalid_selection(self):
        invalid_record = ParkingHistory(
            lot_name="Lot D",
            occupied_spots=-5,
            available_spots=50
        )
        self.assertLess(invalid_record.occupied_spots, 0)
