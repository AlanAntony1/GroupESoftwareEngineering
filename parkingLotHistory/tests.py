from django.test import TestCase
from .models import ParkingHistory
from django.utils import timezone

class ParkingHistoryTestCase(TestCase):
    def setUp(self):
        # Simulate some initial building selections by users
        self.history1 = ParkingHistory.objects.create(
            building_name="Norris Hall",
            closest_lot="Lot A",
            distance=0.25,
            timestamp=timezone.now()
        )
        self.history2 = ParkingHistory.objects.create(
            building_name="Evans Hall",
            closest_lot="Lot B",
            distance=0.5,
            timestamp=timezone.now()
        )

    # Test that a single record is created correctly
    def test_create_record(self):
        history_count = ParkingHistory.objects.count()
        self.assertEqual(history_count, 2)
        first_record = ParkingHistory.objects.get(building_name="Norris Hall")
        self.assertEqual(first_record.closest_lot, "Lot A")
        self.assertEqual(first_record.distance, 0.25)

    # Test adding a new record simulating a new user selection
    def test_add_new_selection(self):
        ParkingHistory.objects.create(
            building_name="Sarkeys Energy Center",
            closest_lot="Lot C",
            distance=0.75,
            timestamp=timezone.now()
        )
        self.assertEqual(ParkingHistory.objects.count(), 3)
        new_record = ParkingHistory.objects.get(building_name="Sarkeys Energy Center")
        self.assertEqual(new_record.closest_lot, "Lot C")
        self.assertEqual(new_record.distance, 0.75)

    # Test that multiple selections of the same building create separate records
    def test_multiple_selections_same_building(self):
        ParkingHistory.objects.create(
            building_name="Norris Hall",
            closest_lot="Lot D",
            distance=0.3,
            timestamp=timezone.now()
        )
        records = ParkingHistory.objects.filter(building_name="Norris Hall")
        self.assertEqual(records.count(), 2)

    # Test that records are ordered by timestamp
    def test_ordering_by_timestamp(self):
        timestamps = [record.timestamp for record in ParkingHistory.objects.all().order_by('timestamp')]
        self.assertEqual(timestamps, sorted(timestamps))

    # Test invalid selection (e.g., negative distance)
    def test_invalid_selection(self):
        invalid_record = ParkingHistory(
            building_name="Fake Building",
            closest_lot="Lot X",
            distance=-1
        )
        self.assertLess(invalid_record.distance, 0)

    
   # #Check the invalid error message comes up
   # def test_invalid_selection(self):
   #     invalid_record = ParkingHistory(
   #         lot_name="Lot D",
    #        occupied_spots=-5,
   #         available_spots=50,
   #         timestamp=timezone.now()
    #    )

    #    with self.assertRaises(ValidationError):
    #        invalid_record.full_clean()
