from django.db.models import QuerySet

from orders.models import Merch
from orders.validators import validate_exsisting_merch


def get_filtered_merch_objects(merch_data: list[dict]) -> list[Merch]:
    """Получаем на входе словарь с данными для мерча, на выходе
    QuerySet с объектами мерча. Также проводится валидация на
    существующие объекты мерча в базе"""
    query = []
    for data in merch_data:
        merch = Merch.objects.get(name=data.get("name"), size=data.get("size"))
        validate_exsisting_merch(merch)
        query.append(merch)
    return query


def modification_of_response_dict(query: list[dict]) -> list[dict]:
    """Агрегация по id амбассадора данных о мерче на выходе.
    Берет все данные, и соединяет мерч по id амбассадора"""
    uniq = set(obj["id"] for obj in query)
    result = []
    all_merch = Merch.objects.all().values("name")
    i = 0
    for id in uniq:
        # Вычисление количествbа таких же id в словаре
        k = sum(1 for q in query if q["id"] == id)
        result.append(
            {
                "id": query[i]["id"],
                "first_name": query[i]["first_name"],
                "last_name": query[i]["last_name"],
                "merch": list(merch_collecting(all_merch, query[0:k])),
                "total": query[i]["total"],
            }
        )
        # Удаление всех записей относящихся к id
        for _ in range(k):
            query.pop(0)
    return result


def merch_collecting(all_merch: QuerySet, query: QuerySet) -> list[dict]:
    """Проходим по всем мерчам и считаем количество каждого в Query"""
    return [
        {
            "name": merch["name"],
            "count": sum(1 for x in query if x["merch_name"] == merch["name"])
        } for merch in all_merch.values("name")]