from django.contrib.admin import register, ModelAdmin

from csvexport.actions import csvexport

from car.models import Car


@register(Car)
class CarDetailsAdmin(ModelAdmin):
    list_display = (
        "brand",
        "model",
        "registration",
    )
    ordering = ("brand", "model", "registration")
    search_fields = ("^brand", "^model", "^registration")
    actions = (csvexport,)
