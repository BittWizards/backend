# Generated by Django 4.2.9 on 2024-02-24 20:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("live", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="push",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
    ]