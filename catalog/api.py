from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Motorcycle, Accessory
from .serializers import MotorcycleSerializer, AccessorySerializer


class MotorcycleViewSet(ReadOnlyModelViewSet):
    queryset = Motorcycle.objects.filter(status="available")
    serializer_class = MotorcycleSerializer


class AccessoryViewSet(ReadOnlyModelViewSet):
    queryset = Accessory.objects.all()
    serializer_class = AccessorySerializer