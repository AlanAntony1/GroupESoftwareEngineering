from django.test import TestCase, Client
from .models import Highlight


# Create your tests here.

class HighlightModelTests(TestCase):
    def testfilterhighlighted(self):
        Highlight.objects.create(spotid="testspot1", isHighlighted=True)
        Highlight.objects.create(spotid="testspot2", isHighlighted=False)
        Highlight.objects.create(spotid="testspot3", isHighlighted=True)

        highlighted = Highlight.objects.filter(isHighlighted=True)
        ids = [h.spotid for h in highlighted]

        self.assertEqual(ids, ["testspot1", "testspot3"])
 
class ToggleMissingIDTests(TestCase):
    def testmissingspotid(self):
        response = self.client.get("/highlight/toggle-spot/")
        self.assertEqual(response.status_code, 400)        

class ToggleSpotFalseToTrueTests(TestCase):
    def setUp(self):
        self.client = Client()
        Highlight.objects.create(spotid="stestspot", isHighlighted=False)

    def test_toggle_false_to_true(self):
        response = self.client.get("/highlight/toggle-spot/?spotid=stestspot")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["newstate"])

        updated = Highlight.objects.get(spotid="stestspot")
        self.assertTrue(updated.isHighlighted)
        
  ## Incorrect Synch test where the fontend has a spot, but the data does not
  
class SyncCreateTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_frontend_has_spot_but_db_missing(self):
        response = self.client.get("/highlight/toggle-spot/?spotid=newspot")
        data = response.json()

        obj = Highlight.objects.get(spotid="newspot")

        self.assertTrue(obj.isHighlighted)
        self.assertTrue(data["newstate"]) 
       


