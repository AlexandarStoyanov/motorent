from django.shortcuts import render
from .models import Motorcycle, Accessory


def rent(request):
    motorcycles = Motorcycle.objects.filter(status="available")
    accessories = Accessory.objects.all()

    return render(request, "rent.html", {
        "motorcycles": motorcycles,
        "accessories": accessories,
    })


def accessories(request):
    accessories = Accessory.objects.all()

    return render(request, "accessories.html", {
        "accessories": accessories,
    })