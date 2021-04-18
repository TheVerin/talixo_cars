from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from car.models import Car
from car.serializers import CarSerializer


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all().order_by("-id")
    serializer_class = CarSerializer
    lookup_field = "special_id"

    def list(self, request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            updated_data = [
                self._remove_fields(
                    serializer=instance,
                    request=request,
                )
                for instance in serializer.data
            ]
            return self.get_paginated_response(updated_data)

    def retrieve(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        updated_data = self._remove_fields(
            serializer=serializer.data,
            request=request,
        )
        return Response(updated_data)

    def _remove_fields(self, serializer, request):
        try:
            if not bool(request.query_params["show_class"]):
                serializer.pop("car_class")
            if not bool(request.query_params["show_hybrid_or_electric"]):
                serializer.pop("hybrid_or_electric")
            return serializer
        except MultiValueDictKeyError:
            serializer.pop("car_class")
            serializer.pop("hybrid_or_electric")
            return serializer
