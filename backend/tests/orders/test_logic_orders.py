import datetime as dt
from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

create_data = {
    "first_name": "Имя",
    "last_name": "Фамилия",
    "middle_name": "Отчество",
    "phone": "7 (917) 123-45-69",
    "country": "Страна",
    "city": "Город1",
    "street_home": "Улица1",
    "post_index": "100001",
    # TODO
    # "sizes": {
    #     "clothes_size": "XL",
    #     "foot_size": "39-41",
    # },
    # TODO
    # "merch": "толстовка",
}


@pytest.mark.django_db
def test_post_and_patch_order(client: APIClient, create_orders):
    url = "/api/v1/orders/"
    data = create_data

    response = client.post(url, data, "application/json")
    print(response.json())
    assert response.status_code == HTTPStatus.CREATED
    data["id"] = 1
    data["status"] = "created"
    data["track_number"] = None
    assert response.json() == data


@pytest.mark.django_db
def test_post_incorrect_order(client: APIClient, create_orders):
    url = "/api/v1/orders/"
    data = create_data
    data.pop("phone")

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_patch_status_order(client: APIClient, create_orders):
    url = "/api/v1/orders/1/"

    now = dt.datetime.now()

    response = client.patch(
        url,
        {"status": "delivered", "delivered_at": now},
        "application/json",
    )
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_patch_status_without_time_order(client: APIClient, create_orders):
    url = "/api/v1/orders/1/"

    response = client.patch(
        url,
        {"status": "delivered"},
        "application/json",
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
