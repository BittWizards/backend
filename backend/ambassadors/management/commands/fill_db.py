from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from openpyxl.reader.excel import load_workbook

from ambassadors.management.commands._import_models import (
    import_actions,
    import_address,
    import_ambass_actions,
    import_ambassadors,
    import_content,
    import_docs,
    import_merch,
    import_orders,
    import_promo,
    import_sizes,
    import_ya_programms,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                input_data = load_workbook("data/test_data.xlsx")
                import_ya_programms(self, input_data["ya_programm"])
                import_actions(self, input_data["actions"])
                import_ambassadors(self, input_data["ambassadors"])
                import_address(self, input_data["address"])
                import_ambass_actions(self, input_data["ambass_actions"])
                import_content(self, input_data["content"])
                import_docs(self, input_data["docs"])
                import_sizes(self, input_data["sizes"])
                import_promo(self, input_data["promo"])
                import_merch(self, input_data["merch"])
                import_orders(self, input_data["orders"])

        except Exception as error:
            raise CommandError(f"Сбой при импорте: {error}")

        self.stdout.write(self.style.SUCCESS("Импорт прошел успешно"))
