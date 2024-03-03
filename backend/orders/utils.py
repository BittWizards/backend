from django.db.models import Q, QuerySet

from orders.models import Merch


def get_filtered_merch_objects(merch_data: dict) -> QuerySet[Merch]:
    """Получаем на входе словарь с данными для мерча, на выходе
    QuerySet с объектами мерча"""
    merch = Merch.objects.filter(
        Q(name__in=(merch.get("name") for merch in merch_data)),
        Q(size__in=(merch.get("size") for merch in merch_data))
        | Q(size__isnull=True),
    )
    return merch


def modification_of_response_dict(query: list[dict]) -> list[dict]:
    """Агрегация по id амбассадора данных о мерче на выходе.
    Берет все данные, и соединяет мерч по id амбассадора"""
    uniq = set(obj['id'] for obj in query)
    result = []
    i = 0
    for id in uniq:
        # Вычисление количествbа таких же id в словаре
        k = sum(1 for q in query if q['id'] == id)
        result.append({
            'id': query[i]['id'],
            'first_name': query[i]['first_name'],
            'last_name': query[i]['last_name'],
            # Добавление мерча относящегося к этому id
            'merch': {
                query[j]['merch_name']: query[j]['count'] for j in range(k)
            }
        })
        # Удаление всех записей относящихся к id
        for _ in range(k):
            query.pop(0)
    return result
