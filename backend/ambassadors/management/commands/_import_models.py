from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import models
from django.utils.timezone import make_aware
from openpyxl.worksheet.worksheet import Worksheet


def import_models(self: BaseCommand, obj: Worksheet, model: models.Model):
    field_names = tuple(obj.iter_rows(1, 1, values_only=True))[0]
    cells = obj.iter_rows(2, values_only=True)

    for values in cells:
        values_dict = {}
        many_to_many_values_dict = {}
        for index, field_name in enumerate(field_names):
            if (
                model._meta.get_field(field_name).__class__.__name__
                == "ManyToManyField"
            ):
                many_to_many_values_dict[field_name] = values[index]
            else:
                value = values[index]
                if isinstance(value, datetime):
                    value = make_aware(value)
                values_dict[field_name] = value

        model_obj, _ = model.objects.get_or_create(**values_dict)

        for field_name in many_to_many_values_dict.keys():
            related_manager = getattr(model_obj, field_name)
            related_manager.set(
                str(many_to_many_values_dict[field_name]).split(", ")
            )

    self.stdout.write(
        self.style.SUCCESS(f"Данные для {model.__qualname__} загружены")
    )
