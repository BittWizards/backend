import datetime as dt
from http import HTTPStatus

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_user_auth(client: APIClient, create_ambassadors):
    url = ""
    now = dt.datetime.utcnow()

    data = {
        "email": "test@example.com",
        "first_name": "Иван",
        "last_name": "Иванов",
        "middle_name": "Иванович",
        "gender": "male",
        "ya_programm": 1,
        "phone": "7 (917) 123-45-69",
        "tg_acc": "ivanov",
        "education": "11 классов",
        "work_now": True,
        "status": "active",
        "created": now,
        "ambassador_actions": [2, 4],
        "address": {
            "country": "Страна",
            "city": "Город1",
            "street_home": "Улица1",
            "post_index": "100001",
        },
        "sizes": {
            "clothes_size": "XL",
            "foot_size": "39-41",
        },
    }

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5
    data["ya_programm"] = {"title": "Programm1", "description": "1"}
    data["ambassador_actions"] = [
        {
            "title": "Actions2",
            "description": "2",
        },
        {
            "title": "Actions4",
            "description": "4",
        },
    ]
    data["id"] = 6
    assert response.json() == data
