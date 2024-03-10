# Generated by Django 4.2.9 on 2024-03-10 06:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="created_date",
            field=models.DateField(
                default=django.utils.timezone.now,
                verbose_name="Дата создания заявки",
            ),
        ),
    ]
