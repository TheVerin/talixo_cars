from rest_framework.viewsets import ModelViewSet

from car.models import Car
from car.serializers import CarSerializer


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all().order_by("-id")
    serializer_class = CarSerializer
    lookup_field = "special_id"
