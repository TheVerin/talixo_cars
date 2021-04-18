from django.test import TestCase
from django.db.utils import IntegrityError

from car.models import Car


class EntryModelTest(TestCase):
    def test_valid_car_model(self):
        entry = Car.objects.create(
            brand="Brand",
            model="Model",
            type="Type",
            registration_number="AAA 4455",
            max_passengers=5,
            production_year=2020,
        )
        self.assertEqual(str(entry), "Brand Model AAA 4455")

    def test_car_model_no_data(self):
        try:
            Car.objects.create()
        except IntegrityError:
            self.assertTrue(True)

    def test_car_model_no_brand(self):
        try:
            Car.objects.create(
                model="Model", type="Type", registration_number="AAA 4455"
            )
        except IntegrityError:
            self.assertTrue(True)
