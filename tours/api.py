import json

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Tour
from .serializers import TourSerializer
from catalog.models import Motorcycle


class TourViewSet(ReadOnlyModelViewSet):
    queryset = Tour.objects.filter(is_active=True).order_by("-id")
    serializer_class = TourSerializer


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

    if not tour_id or not full_name or not email or not phone or not people or not motorcycle_id:
        return JsonResponse({"ok": False, "error": "Missing required fields"}, status=400)

    tour = Tour.objects.filter(id=tour_id, is_active=True).first()
    moto = Motorcycle.objects.filter(id=motorcycle_id).first()

    if not tour:
        return JsonResponse({"ok": False, "error": "Tour not found"}, status=404)

    if not moto:
        return JsonResponse({"ok": False, "error": "Motorcycle not found"}, status=404)

    admin_email = (
        getattr(settings, "TOURS_ADMIN_EMAIL", None)
        or getattr(settings, "ADMIN_EMAIL", None)
        or settings.DEFAULT_FROM_EMAIL
    )

    body = (
        f"ИМЕ: {full_name}\n"
        f"EMAIL: {email}\n"
        f"ТЕЛЕФОН: {phone}\n"
        f"БРОЙ УЧАСТНИЦИ: {people}\n"
        f"ТУР: {tour.title}\n"
        f"МОТОЦИКЛЕТ: {moto}\n"
        f"АКСЕСОАРИ: {', '.join(map(str, accessories)) if accessories else '-'}\n"
        f"БЕЛЕЖКИ: {notes if notes else '-'}\n"
    )

    send_mail(
        f"Ново запитване за тур: {tour.title}",
        body,
        settings.DEFAULT_FROM_EMAIL,
        [admin_email],
        fail_silently=False,
    )

    return JsonResponse({"ok": True})