from django.contrib.admin import ModelAdmin, register

from csvexport.actions import csvexport

from car.models import Car


@register(Car)
class CarDetailsAdmin(ModelAdmin):
    list_display = (
        "brand",
        "model",
        "registration_number",
    )
    ordering = ("brand", "model", "registration_number")
    search_fields = ("^brand", "^model", "^registration_number")
    actions = (csvexport,)
