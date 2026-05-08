from rest_framework import serializers
from .models import Motorcycle, Accessory


class MotorcycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorcycle
        fields = "__all__"


class AccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields = "__all__"