from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from car.models import Car


class CarSerializer(ModelSerializer):
    registration = SerializerMethodField()

    class Meta:
        model = Car
        fields = (
            "special_id",
            "brand",
            "model",
            "type",
            "registration",
            "max_passengers",
            "production_year",
            "car_class",
            "hybrid_or_electric",
        )

    def get_registration(self, current_car: Car) -> str:
        return current_car.registration.upper()
