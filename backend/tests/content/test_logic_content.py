from http import HTTPStatus

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_post_and_patch_content(client: APIClient, create_ambassadors):
    url = "api/v1/content"
    data = {
        "ambassador_id": 1,
        "telegram": "example",
        "link": "https://example.com",
        "files": None,
    }

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.CREATED
    data["id"] = 1
    data["status"] == "in pending"
    assert response.json() == data

    url = "api/v1/ambassador/1/content/1"
    response = client.patch(url, {"status": "accepted"}, "application/json")
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_post_incorrect_content(client: APIClient, create_ambassadors):
    url = "api/v1/content"
    data = {
        "ambassador_id": 1,
        "telegram": "example",
        "link": "http://example.com",  # сайт без сертификата
        "files": None,
    }

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_post_and_delete_promocode(client: APIClient, create_ambassadors):
    url = "api/v1/promocodes"
    data = {
        "ambassador_id": 1,
        "name": "example",
    }

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == data

    url = "api/v1/promocodes/example"
    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.django_db
def test_post_duplicate_promocode(client: APIClient, create_ambassadors):
    url = "api/v1/promocodes"
    data = {
        "ambassador_id": 1,
        "name": "example",
    }

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == data

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
