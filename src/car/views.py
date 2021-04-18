from rest_framework.viewsets import ModelViewSet

from car.models import Car
from car.serializers import CarSerializer


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = "special_id"

    def get_serializer_context(self):
        context = super(CarViewSet, self).get_serializer_context()
        context.update(
            {
                "car_class": self.kwargs["car_class"],
                "hybrid_or_electric": self.kwargs["hybrid_or_electric"],
            }
        )
        return context
