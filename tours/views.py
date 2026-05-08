from django.shortcuts import render
from .models import Tour
from catalog.models import Motorcycle, Accessory


def tours(request):
    tours_list = Tour.objects.filter(is_active=True).order_by("-id")
    motorcycles = Motorcycle.objects.filter(status="available")
    accessories = Accessory.objects.all()

    return render(request, "tours.html", {
        "tours": tours_list,
        "motorcycles": motorcycles,
        "accessories": accessories,
    })