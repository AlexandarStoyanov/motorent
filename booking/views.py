from rest_framework.viewsets import ModelViewSet
from .models import Booking
from .serializers import BookingSerializer

from django.shortcuts import render

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all().order_by("-created_at")
    serializer_class = BookingSerializer


def booking_payment_success(request):
    return render(request, "booking/payment_success.html")


def booking_payment_cancel(request):
    return render(request, "booking/payment_cancel.html")