from django.contrib import admin
from .models import Tour

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("title", "days", "km", "max_people", "level", "price", "is_active")
    list_filter = ("level", "is_active")
    search_fields = ("title",)
