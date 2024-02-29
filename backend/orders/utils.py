from django.db.models import Q, QuerySet

from orders.models import Merch


def get_filtered_merch_objects(merch_data: dict) -> QuerySet[Merch]:
    """Получаем на входе словарь с данными для мерча, на выходе
    QuerySet с объектами мерча"""
    merch = Merch.objects.filter(
        Q(name__in=(merch.get('name') for merch in merch_data)),
        Q(
            size__in=(merch.get('size') for merch in merch_data)
        ) | Q(size__isnull=True)
    )
    return merch