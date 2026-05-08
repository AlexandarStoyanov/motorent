from django.shortcuts import render
from catalog.models import Motorcycle


def home(request):
    motorcycles = Motorcycle.objects.filter(status="available")
    return render(request, "home.html", {"motorcycles": motorcycles})