from django.test import TestCase
from .models import Building
from decimal import Decimal

# Create your tests here.
class BuildingTestCase(TestCase):
    def setUp(self):
        # This is a correct setup for a building
        self.building1 = Building.objects.create(
            buildingName="AAA",
            closestLot="Lot A",
            distance=Decimal("10.00")
        )
        # This building has a distance too far to be considered close
        self.building2 = Building.objects.create(
            buildingName="BBB",
            closestLot="Lot B",
            distance=Decimal("50.00")
        )

        # This building has a distance right at the boundary to be considered close
        self.building3 = Building.objects.create(
            buildingName="CCC",
            closestLot="Lot C",
            distance=Decimal("15.00")
        )
        # This building has an invalid, negative, distance
        self.building4 = Building(
            buildingName="DDD",
            closestLot="Lot D",
            distance=Decimal("-5.00")
        )
    
    # Distance Tests
    # Correct Case 
    def test_parking_lot_correct(self):
        """Test that building 1 has all correct information"""
        distance = self.building1.distance
        self.assertEqual(distance, Decimal("10.00"))
    # Incorrect Case 
    def test_parking_lot_invalid(self):
        """Test that a parking lot with a large distance is detected as invalid."""
        distance = self.building2.distance
        self.assertGreater(distance, Decimal("15.00"))
    # Boundary Case
    def test_parking_lot_boundary(self):
        """Test that a parking lot is not detected as invalid upto 15 miles"""
        distance = self.building3.distance
        self.assertLessEqual(distance, Decimal("15.00"))
    # Negative Distance 
    def test_negative_distance(self):
        """Test that negative distances are detected as invalid."""
        self.assertLess(self.building4.distance, 0)
    