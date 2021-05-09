import uuid

from django.db.models import (
    BooleanField,
    CharField,
    Model,
    PositiveSmallIntegerField,
    UUIDField,
)


CLASSES = [
    ("ECONOMIC", "ECONOMIC"),
    ("BUSINESS", "BUSINESS"),
    ("FIRST", "FIRST"),
]


class Car(Model):
    special_id = UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registration_number = CharField(max_length=10, blank=True, unique=True)
    max_passengers = PositiveSmallIntegerField(blank=True)
    production_year = PositiveSmallIntegerField(blank=True)
    brand = CharField(max_length=20)
    model = CharField(max_length=20)
    type = CharField(max_length=20)
    car_class = CharField(max_length=20, choices=CLASSES, blank=True)
    hybrid_or_electric = BooleanField(blank=True, default=False)

    def __str__(self) -> str:
        return f"{self.brand} {self.model} {self.registration_number}"
