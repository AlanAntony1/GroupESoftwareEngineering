from django.test import TestCase
from .models import Highlight
import time
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your tests here.

class HighlightButtonTest(TestCase):
    def  setUp(self):
        "Testing valid button input"
        self.obj = Highlight.objects.create(
            button = False,
            isHighlighted=False,
            lastPressed=timezone.now()
        )

        self.assertEqual(self.obj.button, False)
        self.assertEqual(self.obj.isHighlighted, False)
        self.assertIsNotNone(self.obj.lastPressed)

    def test_initial_state(self):
        self.assertFalse(self.obj.button)
        self.assertFalse(self.obj.isHighlighted)


    def test_button_press_changes_state(self):
        old_time = self.obj.lastPressed
        self.obj.press_button()


        self.assertTrue(self.obj.button)
        self.assertTrue(self.obj.isHighlighted)
        self.assertGreater(self.obj.lastPressed, old_time)


    def test_button_toggle_highlight(self):
        self.obj.press_button()

        self.assertTrue(self.obj.isHighlighted)

        self.obj.press_button()

        self.assertFalse(self.obj.isHighlighted)

    def test_button_time_updates_each_press(self):
        first_time = self.obj.lastPressed
        time.sleep(0.5)
        self.obj.press_button()
        self.assertGreater(self.obj.lastPressed, first_time)



        
       


