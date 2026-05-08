from django.db import models
from catalog.models import Motorcycle

class Booking(models.Model):
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE, related_name="bookings")

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone_number = models.CharField(max_length=40, blank=True)

    start_date = models.DateField()
    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.motorcycle} ({self.start_date} to {self.end_date})"
