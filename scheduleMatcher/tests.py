from django.test import TestCase

# Create your tests here.
# scheduleMatcher/tests.py

from datetime import time

from availableLots.models import AvailableLots
from .ai_matcher import ScheduleItem, recommend_for_schedule


class AIScheduleMatcherAccuracyTest(TestCase):
    """
    Verify that, for a set of known schedule items (test cases),
    the AI Schedule Matcher recommends the correct lot with
    accuracy >= 70%.
    """

    def setUp(self):
        # Set up OU commuter garages that match LOT_COORDS
        self.asp = AvailableLots.objects.create(
            lot_name="Asp Avenue Parking Facility",
            total_spaces=300,
            available_spaces=200,  # moderately full
        )
        self.elm = AvailableLots.objects.create(
            lot_name="Elm Avenue Parking Facility",
            total_spaces=250,
            available_spaces=150,
        )

        # Synthetic "gold" test schedule
        self.items = [
            # Near DEV → Asp Avenue (closer)
            ScheduleItem(
                course="CS3203",
                building="DEV",
                day_of_week="Mon",
                start_time=time(9, 0),
                end_time=time(9, 50),
                pass_type="COMMUTER",
            ),
            # Near GOULD → Elm Avenue
            ScheduleItem(
                course="ARCH2013",
                building="GOULD",
                day_of_week="Tue",
                start_time=time(10, 30),
                end_time=time(11, 45),
                pass_type="COMMUTER",
            ),
            # Near PHSC → Elm Avenue
            ScheduleItem(
                course="PHYS2514",
                building="PHSC",
                day_of_week="Wed",
                start_time=time(13, 30),
                end_time=time(14, 20),
                pass_type="COMMUTER",
            ),
        ]

        self.expected_lots = [
            "Asp Avenue Parking Facility",
            "Elm Avenue Parking Facility",
            "Elm Avenue Parking Facility",
        ]

    def test_schedule_matcher_accuracy_at_least_70_percent(self):
        # Get model recommendations
        recs = recommend_for_schedule(self.items)

        correct = 0
        total = len(self.items)

        for rec, expected in zip(recs, self.expected_lots):
            if rec["recommended_lot"] == expected:
                correct += 1

        accuracy = correct / total

        # Backlog acceptance: > 70% accuracy on test cases
        self.assertGreaterEqual(
            accuracy,
            0.70,
            msg=f"AI Schedule Matcher accuracy too low: {accuracy:.2%}",
        )
