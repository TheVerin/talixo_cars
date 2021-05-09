from rest_framework.serializers import ModelSerializer

from car.models import Car


class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = (
            "special_id",
            "brand",
            "model",
            "type",
            "registration_number",
            "max_passengers",
            "production_year",
            "car_class",
            "hybrid_or_electric",
        )
