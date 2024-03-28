from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from openpyxl.reader.excel import load_workbook

from ambassadors.management.commands._import_models import import_models
from ambassadors.models import (
    Actions,
    Ambassador,
    AmbassadorActions,
    AmbassadorAddress,
    AmbassadorSize,
    YandexProgramm,
)
from content.models import Content, Documents, Promocode
from orders.models import Merch, Order


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                input_data = load_workbook("data/test_data.xlsx")
                import_models(self, input_data["ya_programm"], YandexProgramm)
                import_models(self, input_data["actions"], Actions)
                import_models(self, input_data["ambassadors"], Ambassador)
                import_models(self, input_data["address"], AmbassadorAddress)
                import_models(
                    self, input_data["ambass_actions"], AmbassadorActions
                )
                import_models(self, input_data["content"], Content)
                import_models(self, input_data["docs"], Documents)
                import_models(self, input_data["sizes"], AmbassadorSize)
                import_models(self, input_data["promo"], Promocode)
                import_models(self, input_data["merch"], Merch)
                import_models(self, input_data["orders"], Order)

        except Exception as error:
            raise CommandError(f"Сбой при импорте: {error}")

        self.stdout.write(self.style.SUCCESS("Импорт прошел успешно"))
