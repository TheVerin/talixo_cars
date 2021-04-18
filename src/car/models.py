import uuid

from django.db.models import (
    CharField,
    Model,
    PositiveSmallIntegerField,
    BooleanField,
    UUIDField,
)

CLASSES = [
    ("E", "ECONOMICS"),
    ("B", "BUSINESS"),
    ("F", "FIRST"),
]


class Car(Model):
    special_id = UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registration = CharField(max_length=10, blank=True)
    max_passengers = PositiveSmallIntegerField(blank=True)
    production_year = PositiveSmallIntegerField(blank=True)
    brand = CharField(max_length=20)
    model = CharField(max_length=20)
    type = CharField(max_length=20)
    car_class = CharField(max_length=20, choices=CLASSES, blank=True)
    hybrid_or_electric = BooleanField(blank=True, default=False)

    def __str__(self) -> str:
        return f"{self.brand} {self.model} {self.registration}"
