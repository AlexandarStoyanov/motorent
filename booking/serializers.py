from decimal import Decimal
from datetime import date

import stripe

from django.conf import settings

from rest_framework import serializers

from .models import Booking
from catalog.models import Motorcycle


class BookingSerializer(serializers.ModelSerializer):

    checkout_url = serializers.CharField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "motorcycle",
            "full_name",
            "email",
            "phone_number",
            "start_date",
            "end_date",
            "payment_method",
            "payment_status",
            "total_price",
            "checkout_url",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "payment_status",
            "total_price",
            "checkout_url",
            "created_at",
        ]

    def create(self, validated_data):

        motorcycle = validated_data["motorcycle"]

        start_date = validated_data["start_date"]
        end_date = validated_data["end_date"]

        payment_method = validated_data.get("payment_method", "onsite")

        days = (end_date - start_date).days

        if days <= 0:
            days = 1

        total_price = Decimal(motorcycle.price_per_day) * days

        booking = Booking.objects.create(
            motorcycle=motorcycle,
            full_name=validated_data["full_name"],
            email=validated_data["email"],
            phone_number=validated_data.get("phone_number", ""),
            start_date=start_date,
            end_date=end_date,
            payment_method=payment_method,
            payment_status="pending" if payment_method == "online" else "onsite",
            total_price=total_price,
        )

        if payment_method == "online":

            stripe.api_key = settings.STRIPE_SECRET_KEY

            request = self.context.get("request")

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="payment",

                customer_email=booking.email,

                line_items=[
                    {
                        "price_data": {
                            "currency": "eur",

                            "product_data": {
                                "name": f"{motorcycle.brand} {motorcycle.model} Rental",
                            },

                            "unit_amount": int(total_price * 100),
                        },

                        "quantity": 1,
                    }
                ],

                metadata={
                    "booking_id": booking.id,
                },

                success_url=request.build_absolute_uri(
                    "/payment-success/"
                ) + "?session_id={CHECKOUT_SESSION_ID}",

                cancel_url=request.build_absolute_uri(
                    "/payment-cancel/"
                ),
            )

            booking.stripe_session_id = session.id
            booking.save()

            booking.checkout_url = session.url

        return booking