import json
import stripe

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Tour, TourBooking
from .serializers import TourSerializer
from catalog.models import Motorcycle


class TourViewSet(ReadOnlyModelViewSet):
    queryset = Tour.objects.filter(is_active=True).order_by("-id")
    serializer_class = TourSerializer

def safe_send_tour_email(subject, body, admin_email):
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [admin_email],
            fail_silently=True,
            timeout=5,
        )
    except Exception as e:
        print("EMAIL ERROR:", e)


@require_POST
@csrf_protect
def send_tour_inquiry(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"ok": False, "error": "Invalid JSON"}, status=400)

    tour_id = data.get("tour_id")
    full_name = (data.get("full_name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    people = data.get("people")
    motorcycle_id = data.get("motorcycle_id")
    accessories = data.get("accessories", [])
    notes = (data.get("notes") or "").strip()
    payment_method = data.get("payment_method", "onsite")

    if payment_method not in ["onsite", "online"]:
        payment_method = "onsite"

    if not tour_id or not full_name or not email or not phone or not people or not motorcycle_id:
        return JsonResponse({"ok": False, "error": "Missing required fields"}, status=400)

    tour = Tour.objects.filter(id=tour_id, is_active=True).first()
    moto = Motorcycle.objects.filter(id=motorcycle_id).first()

    if not tour:
        return JsonResponse({"ok": False, "error": "Tour not found"}, status=404)

    if not moto:
        return JsonResponse({"ok": False, "error": "Motorcycle not found"}, status=404)

    try:
        people_count = int(people)
    except Exception:
        people_count = 1

    if people_count < 1:
        people_count = 1

    total_price = tour.price * people_count

    tour_booking = TourBooking.objects.create(
        tour=tour,
        motorcycle=moto,
        full_name=full_name,
        email=email,
        phone=phone,
        people=people_count,
        accessories=accessories,
        notes=notes,
        payment_method=payment_method,
        payment_status="pending" if payment_method == "online" else "onsite",
        total_price=total_price,
    )

    admin_email = (
        getattr(settings, "TOURS_ADMIN_EMAIL", None)
        or getattr(settings, "ADMIN_EMAIL", None)
        or settings.DEFAULT_FROM_EMAIL
    )

    subject = f"Ново записване за тур: {tour.title}"

    body = (
        f"BOOKING ID: {tour_booking.id}\n"
        f"ИМЕ: {full_name}\n"
        f"EMAIL: {email}\n"
        f"ТЕЛЕФОН: {phone}\n"
        f"БРОЙ УЧАСТНИЦИ: {people_count}\n"
        f"ТУР: {tour.title}\n"
        f"МОТОЦИКЛЕТ: {moto}\n"
        f"АКСЕСОАРИ: {', '.join(map(str, accessories)) if accessories else '-'}\n"
        f"ПЛАЩАНЕ: {'Онлайн' if payment_method == 'online' else 'На място'}\n"
        f"СТАТУС НА ПЛАЩАНЕ: {tour_booking.payment_status}\n"
        f"ОБЩА СУМА: €{total_price}\n"
        f"БЕЛЕЖКИ: {notes if notes else '-'}\n"
    )

    if payment_method == "online":
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="payment",
                customer_email=email,
                line_items=[
                    {
                        "price_data": {
                            "currency": "eur",
                            "product_data": {
                                "name": f"{tour.title} Tour",
                                "description": f"{people_count} participant(s)",
                            },
                            "unit_amount": int(total_price * 100),
                        },
                        "quantity": 1,
                    }
                ],
                metadata={
                    "type": "tour_booking",
                    "tour_booking_id": str(tour_booking.id),
                    "tour_id": str(tour.id),
                    "full_name": full_name,
                    "email": email,
                    "phone": phone,
                    "people": str(people_count),
                    "motorcycle_id": str(moto.id),
                    "accessories": ",".join(map(str, accessories)),
                    "notes": notes,
                },
                success_url=request.build_absolute_uri(
                    f"/payment-success/?tour_booking_id={tour_booking.id}"
                ),
                cancel_url=request.build_absolute_uri(
                    f"/payment-cancel/?tour_booking_id={tour_booking.id}"
                ),
            )

        except Exception as e:
            tour_booking.payment_status = "failed"
            tour_booking.save()
            return JsonResponse({"ok": False, "error": str(e)}, status=500)

        tour_booking.stripe_session_id = session.id
        tour_booking.save()

        body += f"\nSTRIPE SESSION: {session.id}\n"
        safe_send_tour_email(subject, body, admin_email)

        return JsonResponse({
            "ok": True,
            "booking_id": tour_booking.id,
            "checkout_url": session.url,
        })

    safe_send_tour_email(subject, body, admin_email)

    return JsonResponse({
        "ok": True,
        "booking_id": tour_booking.id,
        "message": "Tour booking created successfully.",
    })