from django.urls import path

from car.views import car_views


urlpatterns = [
    path("", car_views, name="car"),
]
