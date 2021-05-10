from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError

from drf_yasg.openapi import IN_QUERY, Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from car.models import Car
from car.serializers import CarSerializer


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all().order_by("-id")
    serializer_class = CarSerializer

    def get_object(self):
        queryset = self.get_queryset()
        try:
            return get_object_or_404(
                queryset, special_id=self.request.query_params["id"]
            )
        except ValidationError:
            raise Http404()

    @swagger_auto_schema(
        manual_parameters=[
            Parameter(
                "show_class",
                IN_QUERY,
                type="str",
                description="Set True to get full data",
            ),
            Parameter(
                "show_hybrid_or_electric",
                IN_QUERY,
                type="str",
                description="Set True to get full data",
            ),
            Parameter(
                "id",
                IN_QUERY,
                type="str",
                description="Set ID to get special car info",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs) -> Response:
        if "id" in request.query_params:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            updated_data = self._remove_fields(
                serializer=serializer.data,
                request=request,
            )
            return Response(updated_data)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        updated_data = [
            self._remove_fields(
                serializer=instance,
                request=request,
            )
            for instance in serializer.data
        ]
        return self.get_paginated_response(updated_data)

    @swagger_auto_schema(
        manual_parameters=[
            Parameter(
                "id",
                IN_QUERY,
                type="str",
                description="Set ID to remove special car info",
                required=True,
            ),
        ]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            Parameter(
                "id",
                IN_QUERY,
                type="str",
                description="Set ID to update special car info",
                required=True,
            ),
        ]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            Parameter(
                "id",
                IN_QUERY,
                type="str",
                description="Set ID to update special car info",
                required=True,
            ),
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def _remove_fields(self, serializer, request):
        try:
            if request.query_params["show_class"] != "True":
                serializer.pop("car_class")
        except MultiValueDictKeyError:
            serializer.pop("car_class")
        try:
            if request.query_params["show_hybrid_or_electric"] != "True":
                serializer.pop("hybrid_or_electric")
            return serializer
        except MultiValueDictKeyError:
            serializer.pop("hybrid_or_electric")
            return serializer


car_views = CarViewSet.as_view(
    {
        "get": "list",
        "post": "create",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)
