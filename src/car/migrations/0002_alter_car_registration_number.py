# Generated by Django 3.2 on 2021-04-18 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("car", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="registration_number",
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
    ]
