from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from car.models import Car
from car.serializers import CarSerializer


class PublicCarAccess(TestCase):
    def setUp(self) -> None:
        self.endpoint_name = "car"

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

    def test_get_all_cars_all_data(self):
        response = self.client.get(
            reverse(self.endpoint_name),
            {"show_class": "True", "show_hybrid_or_electric": "True"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("car_class" in response.data["results"][0].keys())

    def test_get_all_cars_without_on_demand_data(self):
        response = self.client.get(
            reverse(self.endpoint_name),
            {"show_class": "", "show_hybrid_or_electric": ""},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse("car_class" in response.data["results"][0].keys())

    def test_get_special_car_all_data(self):

        response = self.client.get(
            reverse(self.endpoint_name),
            {
                "id": self.special_id,
                "show_class": "True",
                "show_hybrid_or_electric": "True",
            },
        )
        from_db = Car.objects.get(special_id=self.special_id)
        serializer = CarSerializer(from_db)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_special_car_without_on_demand_data(self):

        response = self.client.get(reverse(self.endpoint_name), {"id": self.special_id})
        from_db = Car.objects.get(special_id=self.special_id)
        serializer = CarSerializer(from_db)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, serializer.data)

    def test_cannot_get_special_car(self):
        response = self.client.get(reverse(self.endpoint_name), {"id": "11"})

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

        response = self.client.post(reverse(self.endpoint_name), payload, format="json")

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

        response = self.client.post(reverse(self.endpoint_name), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        response = self.client.delete(f"/v1/car/?id={self.special_id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update(self):
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
        response = self.client.put(
            f"/v1/car/?id={self.special_id}", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        payload = {
            "registration_number": "AAA 1011",
            "max_passengers": 5,
            "production_year": 2010,
        }
        response = self.client.patch(
            f"/v1/car/?id={self.special_id}", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
