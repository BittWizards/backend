from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

create_data = {
    "first_name": "Иван",
    "last_name": "Иванов",
    "middle_name": "Иванович",
    "gender": "male",
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
    "ya_programm": 1,
    "goal": "Закончить",
    "education": "11 классов",
    "work_now": "Кремль",
    "email": "test@example.com",
    "phone": "7 (917) 123-45-69",
    "tg_acc": "ivanov",
    "ambassador_actions": [2, 4],
}

# @pytest.mark.django_db
# def test_test(client: APIClient, create_ambassadors):
#     url = ""
#     now = dt.datetime.utcnow()

#     data = {
#         "email": "test@example.com",
#         "first_name": "Иван",
#         "last_name": "Иванов",
#         "middle_name": "Иванович",
#         "gender": "male",
#         "ya_programm": 1,
#         "phone": "7 (917) 123-45-69",
#         "tg_acc": "ivanov",
#         "education": "11 классов",
#         "work_now": True,
#         "status": "active",
#         "created": now,
#         "ambassador_actions": [2, 4],
#         "address": {
#             "country": "Страна",
#             "city": "Город1",
#             "street_home": "Улица1",
#             "post_index": "100001",
#         },
#         "sizes": {
#             "clothes_size": "XL",
#             "foot_size": "39-41",
#         },
#     }

#     response = client.post(url, data, "application/json")
#     assert response.status_code == HTTPStatus.OK
#     assert isinstance(response.json(), list)
#     assert len(response.json()) == 5
#     data["ya_programm"] = {"title": "Programm1", "description": "1"}
#     data["ambassador_actions"] = [
#         {
#             "title": "Actions2",
#             "description": "2",
#         },
#         {
#             "title": "Actions4",
#             "description": "4",
#         },
#     ]
#     data["id"] = 6
#     assert response.json() == data


@pytest.mark.django_db
def test_create_ambassador(client: APIClient, create_ambassadors):
    url = "api/v1/ambassadors"

    data = create_data

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.CREATED
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
    data["status"] = "active"
    assert response.json() == data


@pytest.mark.django_db
def test_create_invalid_ambassador(client: APIClient, create_ambassadors):
    url = "api/v1/ambassadors"
    data = create_data
    data["sizes"]["clothes_size"] = "XXXL"

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST

    data = create_data
    data[""]


@pytest.mark.django_db
def test_patch_ambassador(client: APIClient, create_ambassadors):
    url = "api/v1/ambassadors/1"

    data = {"status": "not active"}

    response = client.patch(url, data, "application/json")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "first_name": "Иван1",
        "last_name": "Иванов1",
        "middle_name": "Иванович1",
        "gender": "male",
        "address": {
            "country": "Страна",
            "city": "Город1",
            "street_home": "Улица1",
            "post_index": "100001",
        },
        "sizes": {
            "clothes_size": "M",
            "foot_size": "35-39",
        },
        "ya_programm": 1,
        "goal": "Закончить",
        "education": "11 классов",
        "work_now": "Кремль",
        "email": "ivan.ivanov1@example.com",
        "phone": "7 (917) 123-45-61",
        "tg_acc": "ivanov1",
        "status": "not active",
        "ambassador_actions": ["Action1", "Action2"],
    }
