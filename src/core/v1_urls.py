from django.urls import include, path


urlpatterns = [
    path("car/", include("car.urls")),
]
