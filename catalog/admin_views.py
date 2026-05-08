from decimal import Decimal

from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Avg
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404

from booking.models import Booking
from .models import Motorcycle, Accessory, DiscountCode, Review


def is_admin_user(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(is_admin_user)
def admin_users(request):
    User = get_user_model()
    search = request.GET.get("q", "").strip()

    users = User.objects.all().order_by("-id")

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(id__icontains=search)
        )

    return render(request, "admin_panel/users.html", {
        "users": users,
        "search": search,
    })


@login_required
@user_passes_test(is_admin_user)
def admin_edit_user(request, pk):
    User = get_user_model()
    edited_user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        edited_user.username = request.POST.get("username", "").strip()
        edited_user.email = request.POST.get("email", "").strip()
        edited_user.first_name = request.POST.get("first_name", "").strip()
        edited_user.last_name = request.POST.get("last_name", "").strip()

        edited_user.is_active = bool(request.POST.get("is_active"))
        edited_user.is_staff = bool(request.POST.get("is_staff"))

        if request.user.is_superuser:
            edited_user.is_superuser = bool(request.POST.get("is_superuser"))

        edited_user.save()
        messages.success(request, "User updated successfully.")

    return redirect("admin_users")


@login_required
@user_passes_test(is_admin_user)
def admin_delete_user(request, pk):
    User = get_user_model()
    deleted_user = get_object_or_404(User, pk=pk)

    if deleted_user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect("admin_users")

    deleted_user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect("admin_users")


@login_required
@user_passes_test(is_admin_user)
def admin_dashboard(request):
    User = get_user_model()

    total_bookings = Booking.objects.count()
    motorcycles_count = Motorcycle.objects.count()
    active_users = User.objects.filter(
        is_staff=False,
        is_superuser=False,
        is_active=True,
    ).count()

    total_revenue = Decimal("0.00")

    bookings_for_revenue = Booking.objects.select_related("motorcycle")

    for booking in bookings_for_revenue:
        if booking.motorcycle and booking.start_date and booking.end_date:
            days = (booking.end_date - booking.start_date).days

            if days <= 0:
                days = 1

            total_revenue += booking.motorcycle.price_per_day * days

    try:
        average_rating = Motorcycle.objects.aggregate(avg=Avg("rating"))["avg"] or 0.0
    except Exception:
        average_rating = 0.0

    recent_bookings = Booking.objects.select_related("motorcycle").order_by("-id")[:5]

    try:
        popular_motorcycles = (
            Motorcycle.objects.annotate(bookings_count=Count("booking"))
            .order_by("-bookings_count", "-id")[:5]
        )
    except Exception:
        popular_motorcycles = Motorcycle.objects.all().order_by("-id")[:5]

    return render(request, "admin_panel/dashboard.html", {
        "total_revenue": total_revenue,
        "total_bookings": total_bookings,
        "active_users": active_users,
        "motorcycles_count": motorcycles_count,
        "average_rating": round(average_rating, 1),
        "recent_bookings": recent_bookings,
        "popular_motorcycles": popular_motorcycles,
    })


@login_required
@user_passes_test(is_admin_user)
def admin_motorcycles(request):
    search = request.GET.get("q", "").strip()
    motorcycles = Motorcycle.objects.all().order_by("-id")

    if search:
        motorcycles = motorcycles.filter(model__icontains=search)

    return render(request, "admin_panel/motorcycles.html", {
        "motorcycles": motorcycles,
        "search": search,
    })


@login_required
@user_passes_test(is_admin_user)
def admin_accessories(request):
    accessories = Accessory.objects.all().order_by("-id")
    return render(request, "admin_panel/accessories.html", {
        "accessories": accessories
    })


@login_required
@user_passes_test(is_admin_user)
def admin_bookings(request):
    search = request.GET.get("q", "").strip()

    bookings = Booking.objects.select_related("motorcycle").order_by("-id")

    if search:
        bookings = bookings.filter(
            Q(full_name__icontains=search) |
            Q(email__icontains=search) |
            Q(motorcycle__brand__icontains=search) |
            Q(motorcycle__model__icontains=search)
        )

    today = timezone.localdate()

    total_bookings = bookings.count()
    completed_bookings = bookings.filter(end_date__lt=today).count()
    pending_bookings = bookings.filter(end_date__gte=today).count()
    cancelled_bookings = 0

    return render(request, "admin_panel/bookings.html", {
        "bookings": bookings,
        "search": search,
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "completed_bookings": completed_bookings,
        "cancelled_bookings": cancelled_bookings,
    })

@login_required
@user_passes_test(is_admin_user)
def admin_delete_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    motorcycle = booking.motorcycle
    booking.delete()

    if motorcycle:
        motorcycle.status = "available"
        motorcycle.save()

    messages.success(request, "Booking deleted successfully. Motorcycle is now available.")
    return redirect("admin_bookings")

@login_required
@user_passes_test(is_admin_user)
def admin_add_accessory(request):
    if request.method == "POST":
        Accessory.objects.create(
            name=request.POST.get("name", "").strip(),
            description=request.POST.get("description", "").strip(),
            category=request.POST.get("category", "").strip(),
            price_per_day=request.POST.get("price", "").strip(),
            in_stock=bool(request.POST.get("in_stock")),
            image=request.FILES.get("image"),
        )
    return redirect("admin_accessories")


@login_required
@user_passes_test(is_admin_user)
def admin_edit_accessory(request, pk):
    acc = get_object_or_404(Accessory, pk=pk)

    if request.method == "POST":
        acc.name = request.POST.get("name", "").strip()
        acc.description = request.POST.get("description", "").strip()
        acc.category = request.POST.get("category", "").strip()

        price = request.POST.get("price", "").strip()
        if price:
            acc.price_per_day = price

        acc.in_stock = bool(request.POST.get("in_stock"))

        if request.FILES.get("image"):
            acc.image = request.FILES.get("image")

        acc.save()

    return redirect("admin_accessories")


@login_required
@user_passes_test(is_admin_user)
def admin_delete_accessory(request, pk):
    acc = get_object_or_404(Accessory, pk=pk)
    acc.delete()
    return redirect("admin_accessories")


@login_required
@user_passes_test(is_admin_user)
def admin_add_motorcycle(request):
    if request.method == "POST":
        brand = request.POST.get("brand", "").strip()
        model = request.POST.get("model", "").strip()
        description = request.POST.get("description", "").strip()
        category = request.POST.get("category", "").strip()
        price_per_day = request.POST.get("price_per_day", "").strip()
        engine_cc = request.POST.get("engine_cc", "").strip()
        status = request.POST.get("status", "available").strip()
        image = request.FILES.get("image")

        if not brand or not model or not price_per_day:
            messages.error(request, "Brand, model and price are required.")
            return redirect("admin_motorcycles")

        motorcycle = Motorcycle.objects.create(
            brand=brand,
            model=model,
            description=description,
            category=category or "sport",
            price_per_day=Decimal(price_per_day),
            engine_cc=int(engine_cc) if engine_cc else 0,
            status=status or "available",
            image=image if image else None,
        )

        messages.success(request, f"{motorcycle.brand} {motorcycle.model} added successfully.")

    return redirect("admin_motorcycles")


@login_required
@user_passes_test(is_admin_user)
def admin_edit_motorcycle(request, pk):
    motorcycle = get_object_or_404(Motorcycle, pk=pk)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price", "").strip()

        if name:
            parts = name.split(" ", 1)
            motorcycle.brand = parts[0]
            motorcycle.model = parts[1] if len(parts) > 1 else ""

        motorcycle.description = description

        if price:
            motorcycle.price_per_day = price

        motorcycle.save()

    return redirect("admin_motorcycles")


@login_required
@user_passes_test(is_admin_user)
def admin_delete_motorcycle(request, pk):
    motorcycle = get_object_or_404(Motorcycle, pk=pk)
    motorcycle.delete()
    messages.success(request, "Motorcycle deleted successfully.")
    return redirect("admin_motorcycles")

@login_required
@user_passes_test(is_admin_user)
def admin_discount_codes(request):
    codes = DiscountCode.objects.all().order_by("-id")

    return render(request, "admin_panel/discount_codes.html", {
        "codes": codes,
    })


@login_required
@user_passes_test(is_admin_user)
def admin_add_discount_code(request):
    if request.method == "POST":
        code = request.POST.get("code", "").strip().upper()
        discount_type = request.POST.get("discount_type", "percent")
        value = request.POST.get("value", "").strip()
        is_active = bool(request.POST.get("is_active"))

        if code and value:
            DiscountCode.objects.create(
                code=code,
                discount_type=discount_type,
                value=Decimal(value),
                is_active=is_active,
            )
            messages.success(request, "Discount code created successfully.")

    return redirect("admin_discount_codes")


@login_required
@user_passes_test(is_admin_user)
def admin_delete_discount_code(request, pk):
    code = get_object_or_404(DiscountCode, pk=pk)
    code.delete()
    messages.success(request, "Discount code deleted successfully.")
    return redirect("admin_discount_codes")

@login_required
@user_passes_test(is_admin_user)
def admin_reviews(request):
    reviews = Review.objects.select_related("motorcycle").order_by("-id")
    motorcycles = Motorcycle.objects.all().order_by("brand", "model")

    return render(request, "admin_panel/reviews.html", {
        "reviews": reviews,
        "motorcycles": motorcycles,
    })


@login_required
@user_passes_test(is_admin_user)
def admin_add_review(request):
    if request.method == "POST":
        motorcycle_id = request.POST.get("motorcycle")
        customer_name = request.POST.get("customer_name", "").strip()
        rating = request.POST.get("rating", "5")
        comment = request.POST.get("comment", "").strip()

        motorcycle = get_object_or_404(Motorcycle, pk=motorcycle_id)

        Review.objects.create(
            motorcycle=motorcycle,
            customer_name=customer_name,
            rating=int(rating),
            comment=comment,
        )

        messages.success(request, "Review added successfully.")

    return redirect("admin_reviews")


@login_required
@user_passes_test(is_admin_user)
def admin_delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    messages.success(request, "Review deleted successfully.")
    return redirect("admin_reviews")