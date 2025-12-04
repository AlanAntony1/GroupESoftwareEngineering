# availableLots/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class AvailableLots(models.Model):
    lot_id = models.AutoField(primary_key=True)
    # unique per campus – for now we enforce globally unique names
    lot_name = models.CharField(max_length=100, unique=True)

    # total_spaces > 0
    total_spaces = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    # available_spaces >= 0; the upper bound (<= total_spaces)
    # is enforced in clean() and update_availability()
    available_spaces = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )

    status = models.CharField(max_length=20, default="Open")
    last_updated = models.DateTimeField(auto_now=True)

    def clean(self):
        """Model-level validation to ensure consistent values."""
        super().clean()
        if self.available_spaces > self.total_spaces:
            raise ValidationError(
                {"available_spaces": "Available spaces cannot exceed total spaces."}
            )

    def update_availability(self, new_count: int) -> None:
        """
        Update available spaces and status.
        Raises:
            ValueError: if new_count is negative or > total_spaces.
        """
        if new_count < 0:
            raise ValueError("Available spaces cannot be negative.")
        if new_count > self.total_spaces:
            raise ValueError("Available spaces cannot exceed total spaces.")

        self.available_spaces = new_count
        self.status = "Full" if new_count == 0 else "Open"
        # run validation before saving
        self.full_clean()
        self.save()

    def occupancy_rate(self) -> float:
        """
        Return how full the lot is as a percentage (0–100).
        Example: 40 available of 100 total → 60.0 (% occupied)
        """
        if self.total_spaces == 0:
            return 0.0
        return round((1 - self.available_spaces / self.total_spaces) * 100, 2)

    def __str__(self) -> str:
        return f"{self.lot_name} - {self.status} ({self.available_spaces}/{self.total_spaces})"
