from ambassadors_project.settings import DOMAIN
from orders.models import Merch
from orders.validators import validate_exsisting_merch


def get_filtered_merch_objects(merch_data: list[dict]) -> list[Merch]:
    """Получаем на входе словарь с данными для мерча, на выходе
    QuerySet с объектами мерча. Также проводится валидация на
    существующие объекты мерча в базе"""
    query = []
    for data in merch_data:
        merch = Merch.objects.filter(
            name=data.get("name"), size=data.get("size") or None
        )
        validate_exsisting_merch(merch)
        query.append(merch[0])
    return query


def editing_response_data(query: list[dict]) -> list[dict]:
    """Добавление недостающего мерча к амбассадору"""
    all_merch = Merch.objects.distinct("name").values("name")
    for obj in query:
        obj["image"] = f"http://{DOMAIN}/media/{obj['image']}"
        [
            obj["merch"].append({"name": merch["name"], "count": 0})
            for merch in all_merch
            if merch["name"]
            not in [product["name"] for product in obj["merch"]]
        ]
    return query
