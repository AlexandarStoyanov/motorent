from django.db import models


class Motorcycle(models.Model):
    CATEGORY_CHOICES = [
        ("sport", "Sport"),
        ("touring", "Touring"),
        ("adventure", "Adventure"),
        ("cruiser", "Cruiser"),
        ("naked", "Naked"),
        ("scooter", "Scooter"),
    ]

    STATUS_CHOICES = [
        ("available", "Available"),
        ("booked", "Booked"),
        ("maintenance", "Maintenance"),
        ("unavailable", "Unavailable"),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="sport")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    engine_cc = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    image = models.ImageField(upload_to="motorcycles/", blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model}"

class Accessory(models.Model):
    CATEGORY_CHOICES = [
        ("helmet", "Helmet"),
        ("gloves", "Gloves"),
        ("gear", "Gear"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to="accessories/", blank=True, null=True)

    def __str__(self):
        return self.name

class DiscountCode(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ("percent", "Percent"),
        ("fixed", "Fixed Amount"),
    ]

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default="percent")
    value = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

class Review(models.Model):
    customer_name = models.CharField(max_length=120)
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.motorcycle}"