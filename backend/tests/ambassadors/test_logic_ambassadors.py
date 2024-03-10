from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

create_data = {
    "first_name": "Иван",
    "last_name": "Иванов",
    "middle_name": "Иванович",
    "gender": "Male",
    "address": {
        "country": "Страна",
        "city": "Город1",
        "street_home": "Улица1",
        "post_index": "100001",
    },
    "size": {
        "clothes_size": "XL",
        "foot_size": "41",
    },
    "ya_programm": "Programm2",
    "actions": [{"title": "Action1"}],
    "purpose": "Закончить",
    "education": "11 классов",
    "work": "Кремль",
    "email": "test@example.com",
    "phone": "7(917)123-45-69",
    "tg_acc": "ivanov",
}


@pytest.mark.django_db
def test_create_ambassador(client: APIClient):
    url = "/api/v1/ambassadors/"

    data = create_data

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["status"] == "Clarify"


@pytest.mark.django_db
def test_create_invalid_size(client: APIClient):
    url = "/api/v1/ambassadors/"
    data = create_data
    data["size"]["clothes_size"] = "XXXL"

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_patch_ambassador(client: APIClient, create_ambassadors):
    url = "/api/v1/ambassadors/1/"

    data = {"status": "Not active"}

    response = client.patch(url, data, "application/json")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["status"] == "Not active"
