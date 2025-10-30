# scheduleInput/tests.py

from django.test import TestCase
from .models import ClassInput
from datetime import time
from django.core.exceptions import ValidationError

class ClassInputModelTests(TestCase):
    def test_create_valid_classinput(self):
        """Test creating a valid ClassInput (ENGR 1413 example)."""
        class_input = ClassInput.objects.create(
            name="ENGR 1413",
            startTime=time(16, 0),    # 4:00 PM
            endTime=time(17, 15),     # 5:15 PM
            days="MW",
            location="Felgar Hall"
        )

        self.assertEqual(class_input.name, "ENGR 1413")
        self.assertEqual(class_input.startTime, time(16, 0))
        self.assertEqual(class_input.endTime, time(17, 15))
        self.assertEqual(class_input.days, "MW")
        self.assertEqual(class_input.location, "Felgar Hall")

    def test_string_representation(self):
        """Test the __str__ method returns the name."""
        class_input = ClassInput(name="ENGR 1413")
        self.assertEqual(str(class_input), "ENGR 1413")

    def test_start_time_before_end_time(self):
        """Test validation fails when startTime >= endTime."""
        class_input = ClassInput(
            name="ENGR 1413",
            startTime=time(17, 15),  # 5:15 PM
            endTime=time(16, 0),     # 4:00 PM
            days="MW",
            location="Felgar Hall"
        )

        with self.assertRaises(ValidationError):
            class_input.full_clean()  # Triggers the clean() validation

    def test_name_length_validation(self):
        """Test that name cannot exceed 10 characters."""
        class_input = ClassInput(
            name="ThisNameIsTooLong",
            startTime=time(8, 0),
            endTime=time(9, 0),
            days="TTh",
            location="Gallogly Hall"
        )

        with self.assertRaises(ValidationError):
            class_input.full_clean()
