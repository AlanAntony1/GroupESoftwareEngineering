from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


class ClassInput(models.Model):

    BUILDING_CHOICES = [
        ("Adams Center", "Adams Center"),
        ("Adams Hall", "Adams Hall"),
        ("Anne and Henry Zarrow Hall", "Anne and Henry Zarrow Hall"),
        ("Armory", "Armory"),
        ("Beatrice Carr Wallace Old Science Hall", "Beatrice Carr Wallace Old Science Hall"),
        ("Bizzell Memorial Library", "Bizzell Memorial Library"),
        ("Boomer Outreach Building", "Boomer Outreach Building"),
        ("Boyd House", "Boyd House"),
        ("Buchanan Hall", "Buchanan Hall"),
        ("Bud Wilkinson House", "Bud Wilkinson House"),
        ("Burton Hall", "Burton Hall"),
        ("Carnegie Building", "Carnegie Building"),
        ("Carpenter Hall", "Carpenter Hall"),
        ("Carson Engineering Center", "Carson Engineering Center"),
        ("Cate Center 1", "Cate Center 1"),
        ("Cate Center 2", "Cate Center 2"),
        ("Cate Center 3", "Cate Center 3"),
        ("Cate Center 4", "Cate Center 4"),
        ("Cate Center Dining Hall", "Cate Center Dining Hall"),
        ("Catlett Music Center", "Catlett Music Center"),
        ("Chemistry Annex", "Chemistry Annex"),
        ("Chemistry Building", "Chemistry Building"),
        ("Collings Hall", "Collings Hall"),
        ("Collums Building", "Collums Building"),
        ("Copeland Hall", "Copeland Hall"),
        ("Couch Center", "Couch Center"),
        ("Couch Restaurants", "Couch Restaurants"),
        ("Cross", "Cross"),
        ("Dale Hall", "Dale Hall"),
        ("Dale Hall Tower", "Dale Hall Tower"),
        ("David L. Boren Hall (The Honors College)", "David L. Boren Hall (The Honors College)"),
        ("Devon Energy Hall", "Devon Energy Hall"),
        ("Donald W. Reynolds Performing Arts Center", "Donald W. Reynolds Performing Arts Center"),
        ("Dunham College", "Dunham College"),
        ("Dunham College and Headington College Dining Halls", "Dunham College and Headington College Dining Halls"),
        ("Ellison Hall", "Ellison Hall"),
        ("Engineering Laboratory", "Engineering Laboratory"),
        ("Evans Hall", "Evans Hall"),
        ("Everest Training Center", "Everest Training Center"),
        ("Facilities Management Complex", "Facilities Management Complex"),
        ("Farzaneh Hall", "Farzaneh Hall"),
        ("Felgar Hall", "Felgar Hall"),
        ("Fine Arts Center", "Fine Arts Center"),
        ("Fred Jones Jr. Art Center", "Fred Jones Jr. Art Center"),
        ("Fred Jones Jr. Museum of Art", "Fred Jones Jr. Museum of Art"),
        ("Gallogly ", "Gallogly "),
        ("Gaylord Family-Oklahoma Memorial Stadium", "Gaylord Family-Oklahoma Memorial Stadium"),
        ("Gaylord Hall", "Gaylord Hall"),
        ("George Lynn Cross Hall", "George Lynn Cross Hall"),
        ("Goddard Health Center", "Goddard Health Center"),
        ("Gould Hall", "Gould Hall"),
        ("Headington College", "Headington College"),
        ("Headington Hall", "Headington Hall"),
        ("Henderson-Tolson Cultural Center", "Henderson-Tolson Cultural Center"),
        ("Jacobs Track and Field Facility", "Jacobs Track and Field Facility"),
        ("Jacobson Hall (The OU Visitor Center)", "Jacobson Hall (The OU Visitor Center)"),
        ("Jim Thorpe Multicultural Center", "Jim Thorpe Multicultural Center"),
        ("Kaufman Hall", "Kaufman Hall"),
        ("Lin Hall", "Lin Hall"),
        ("Lissa and Cy Wagner Hall", "Lissa and Cy Wagner Hall"),
        ("McCasland Field House", "McCasland Field House"),
        ("Monnet Hall", "Monnet Hall"),
        ("Mosier Indoor Athletic Facility", "Mosier Indoor Athletic Facility"),
        ("Murray Case Sells Swim Center", "Murray Case Sells Swim Center"),
        ("Nielsen Hall", "Nielsen Hall"),
        ("Noble Electron Microscopy Laboratory", "Noble Electron Microscopy Laboratory"),
        ("Nuclear Engineering Laboratory", "Nuclear Engineering Laboratory"),
        ("Observatory and Landscape Department", "Observatory and Landscape Department"),
        ("OCCE James P. Pappas Administration Building", "OCCE James P. Pappas Administration Building"),
        ("OCCE McCarter Hall of Advanced Studies", "OCCE McCarter Hall of Advanced Studies"),
        ("OCCE Thurman J. White Forum Building", "OCCE Thurman J. White Forum Building"),
        ("Oklahoma Memorial Union", "Oklahoma Memorial Union"),
        ("Old Faculty Club", "Old Faculty Club"),
        ("OU Bookstore", "OU Bookstore"),
        ("Parking Services Office", "Parking Services Office"),
        ("Physical Sciences Center", "Physical Sciences Center"),
        ("Price Hall", "Price Hall"),
        ("Rawl Engineering Practice Facility", "Rawl Engineering Practice Facility"),
        ("Richards Hall", "Richards Hall"),
        ("Robertson Hall", "Robertson Hall"),
        ("Sarkeys Energy Center", "Sarkeys Energy Center"),
        ("Sarkeys Fitness Center", "Sarkeys Fitness Center"),
        ("Sooner Card Office", "Sooner Card Office"),
        ("Sooner Suites", "Sooner Suites"),
        ("Sutton Hall", "Sutton Hall"),
        ("The Switzer Center", "The Switzer Center"),
        ("Wagner Dining Facility", "Wagner Dining Facility"),
        ("Walker Center", "Walker Center"),
        ("Whitehand Hall", "Whitehand Hall"),
    ]
    name = models.CharField(max_length = 20)
    startTime = models.TimeField()
    endTime = models.TimeField()
    days = models.CharField(max_length = 10)
    location = models.CharField(max_length=50, choices=BUILDING_CHOICES, default="Unknown")
    
    arrival_time = models.TimeField(blank=True, null=True)
    
    """closest_parking = models.CharField(max_length = 20, default = "Unknown")"""

    def calculate_arrival_time(self):
    
        class_start = datetime.combine(datetime.today(), self.startTime)
        """
        if class starts between 11am and 2pm arrive 25 minutes early
        """
        ten_am = datetime.combine(datetime.today(), datetime.strptime("10:00", "%H:%M").time())
        two_pm = datetime.combine(datetime.today(), datetime.strptime("14:00", "%H:%M").time())
        if ten_am <= class_start <= two_pm:
            recommended = class_start - timedelta(minutes=25)
        else:
            recommended = class_start - timedelta(minutes=15)
        return recommended.time()
    
    def save(self, *args, **kwargs):
        # Automatically calculates arrival_time every time object saves
        if self.startTime:
            self.arrival_time = self.calculate_arrival_time()
        super().save(*args, **kwargs)
    
    def clean(self):
        """Ensure that startTime is before endTime."""
        if self.startTime and self.endTime and self.startTime >= self.endTime:
            raise ValidationError("Start time must be before end time.")

    def __str__(self):
        return self.name
