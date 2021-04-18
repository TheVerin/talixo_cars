from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.urls import reverse

from car.models import Car
from car.serializers import CarSerializer


class PublicCarAccess(TestCase):
    def setUp(self) -> None:
        self.list = "car-list"
        self.detail = "car-detail"

        self.client = APIClient()

        for value in range(10):
            car = Car.objects.create(
                registration_number=f"AAA 00{value}",
                max_passengers=5,
                production_year=2010,
                brand="Brand",
                model="Model",
                type="Sedan",
                car_class="ECONOMIC",
                hybrid_or_electric=True,
            )
            self.special_id = car.special_id

    def test_get_all_cars(self):
        response = self.client.get(reverse(self.list))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_special_car(self):

        response = self.client.get(
            reverse(self.detail, kwargs={"special_id": self.special_id})
        )
        from_db = Car.objects.get(special_id=self.special_id)
        serializer = CarSerializer(from_db)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_cannot_get_special_car(self):
        response = self.client.get(reverse(self.detail, kwargs={"special_id": "11"}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_payload(self):
        payload = {
            "registration_number": "AAA 1000",
            "max_passengers": 5,
            "production_year": 2010,
            "brand": "Brand",
            "model": "Model",
            "type": "Sedan",
            "car_class": "ECONOMIC",
            "hybrid_or_electric": True,
        }

        response = self.client.post(reverse(self.list), payload, format="json")

        from_db = Car.objects.latest("pk")
        serializer = CarSerializer(from_db)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            serializer.data["registration_number"],
            payload["registration_number"].upper(),
        )

    def test_create_invalid_payload(self):
        payload = {
            "registration_number": "AAA 1000",
            "max_passengers": -5,
            "production_year": -2010,
            "brand": "Brand",
            "model": "Model",
            "type": "Sedan",
            "car_class": "ECONOMIC",
            "hybrid_or_electric": True,
        }

        response = self.client.post(reverse(self.list), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        response = self.client.delete(
            reverse(self.detail, kwargs={"special_id": self.special_id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
