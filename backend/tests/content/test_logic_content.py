from http import HTTPStatus

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_post_and_patch_content(client: APIClient, create_ambassadors):
    url = "/api/v1/content/"
    data = {
        "name": "Алексий",
        "tg_acc": "ivanov1",
        "link": "https://example.com",
        "files": "",
    }

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["accepted"] is False

    url = "/api/v1/content/1/"
    response = client.patch(url, {"status": "accepted"}, "application/json")
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_post_incorrect_content(client: APIClient, create_ambassadors):
    url = "/api/v1/content/"
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
    url = "/api/v1/promocodes/"
    data = {
        "ambassador": 1,
        "promocode": "EXAMPLE",
    }

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.CREATED

    url = "/api/v1/promocodes/1/"
    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.django_db
def test_post_incorrect_promocode(client: APIClient, create_ambassadors):
    url = "/api/v1/promocodes/"
    data = {
        "ambassador": 1,
        "promocode": "ffffff",
    }
    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
