from django.contrib import admin
from .models import Tour, TourBooking


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("title", "days", "km", "max_people", "level", "price", "is_active")
    list_filter = ("level", "is_active")
    search_fields = ("title",)


@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "tour",
        "people",
        "payment_method",
        "payment_status",
        "total_price",
        "created_at",
    )

    list_filter = (
        "payment_method",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "full_name",
        "email",
    )