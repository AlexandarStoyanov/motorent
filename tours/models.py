from django.db import models

class Tour(models.Model):
    LEVEL_CHOICES = [
        ("easy", "Easy"),
        ("mid", "Mid"),
        ("hard", "Hard"),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField()
    image = models.ImageField(upload_to="tours/", blank=True, null=True)

    days = models.PositiveIntegerField(default=1)
    km = models.PositiveIntegerField(default=0)
    max_people = models.PositiveIntegerField(default=1)

    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default="mid")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
class TourBooking(models.Model):
    PAYMENT_METHODS = [
        ("onsite", "On Site"),
        ("online", "Online"),
    ]

    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("onsite", "On Site"),
        ("failed", "Failed"),
    ]

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="bookings")
    motorcycle = models.ForeignKey("catalog.Motorcycle", on_delete=models.SET_NULL, null=True, blank=True)

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)

    people = models.PositiveIntegerField(default=1)
    accessories = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="onsite")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="onsite")

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.tour.title}"