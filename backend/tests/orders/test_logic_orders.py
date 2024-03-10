import datetime as dt
from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

create_data = {
    "ambassador": 1,
    "first_name": "Имя",
    "last_name": "Фамилия",
    "middle_name": "Отчество",
    "phone": "7(917)123-45-69",
    "country": "Страна",
    "city": "Город1",
    "street_home": "Улица1",
    "post_index": "100001",
    "merch": [{"name": "Толстовка", "size": "XL"}],
    "comment": "hjhjh",
}


@pytest.mark.django_db
def test_post_order(client: APIClient, create_ambassadors, create_merch):
    url = "/api/v1/orders/"
    data = create_data

    response = client.post(url, data, "application/json")

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_patch_order(client: APIClient, create_orders):
    url = "/api/v1/orders/1/"

    data = dict(status="shipped", track_number="5415gfdgg55")
    response = client.patch(url, data, "application/json")
    assert response.status_code == HTTPStatus.OK


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
        {"status": "delivered", "delivered_date": now},
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
