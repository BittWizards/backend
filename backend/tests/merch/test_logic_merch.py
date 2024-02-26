from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

create_data = {
    "ambassador_id": 1,
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
    "merch_type": "толстовка",
    "email": "test@example.com",
    "phone": "7 (917) 123-45-69",
    "tg_acc": "ivanov",
}


@pytest.mark.django_db
def test_post_and_patch_merch(client: APIClient, create_ambassadors):
    url = "api/v1/merch"
    data = create_data

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.CREATED
    data["id"] = 1
    data["status"] = "created"
    data["track_number"] = None
    assert response.json() == data

    url = "api/v1/ambassador/1/content/1"
    response = client.patch(
        url,
        {"status": "delivered", "track_number": "123h"},
        "application/json",
    )
    assert response.status_code == HTTPStatus.OK
    data["status"] == "delivered"
    assert response.json() == data


@pytest.mark.django_db
def test_post_incorrect_merch(client: APIClient, create_ambassadors):
    url = "api/v1/merch"
    data = create_data
    data.pop("address")

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
