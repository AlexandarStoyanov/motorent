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
