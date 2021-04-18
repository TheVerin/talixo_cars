# Generated by Django 3.2 on 2021-04-18 14:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Car",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "special_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("registration_number", models.CharField(blank=True, max_length=10)),
                ("max_passengers", models.PositiveSmallIntegerField(blank=True)),
                ("production_year", models.PositiveSmallIntegerField(blank=True)),
                ("brand", models.CharField(max_length=20)),
                ("model", models.CharField(max_length=20)),
                ("type", models.CharField(max_length=20)),
                (
                    "car_class",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("ECONOMIC", "ECONOMIC"),
                            ("BUSINESS", "BUSINESS"),
                            ("FIRST", "FIRST"),
                        ],
                        max_length=20,
                    ),
                ),
                ("hybrid_or_electric", models.BooleanField(blank=True, default=False)),
            ],
        ),
    ]
