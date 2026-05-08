from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from booking.models import Booking
from .models import Profile
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()

            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

@login_required
def profile(request):
    user = request.user
    profile_obj, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()

        if full_name:
            parts = full_name.split(" ", 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ""
        else:
            user.first_name = ""
            user.last_name = ""

        profile_obj.phone_number = phone_number

        user.save()
        profile_obj.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    return render(request, "profile.html", {"profile": profile_obj})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        email=request.user.email
    ).select_related("motorcycle").order_by("-id")

    return render(request, "my_bookings.html", {
        "bookings": bookings
    })