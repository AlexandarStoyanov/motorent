from .models import Booking

ACTIVE_STATUSES = ("pending", "confirmed")

def is_motorcycle_available(motorcycle_id, start_date, end_date):
    # overlap ако: start <= existing_end AND end >= existing_start
    return not Booking.objects.filter(
        motorcycle_id=motorcycle_id,
        status__in=ACTIVE_STATUSES,
        start_date__lte=end_date,
        end_date__gte=start_date,
    ).exists()
