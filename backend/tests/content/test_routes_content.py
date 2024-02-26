from http import HTTPStatus

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_all_content(client: APIClient, create_content):
    def assert_instances(instances):
        for element, index in enumerate(instances):
            assert element["id"] == index + 1
            assert "user_pic" in element
            assert element["status"] == "active"
            assert element["first_name"] == f"Иван{index + 1}"
            assert element["last_name"] == f"Иванов{index + 1}"
            assert element["tg_acc"] == f"ivanov{index + 1}"

            assert isinstance(element["content_count"], list)
            assert element["content_count"]["reviews"] == 1
            assert element["content_count"]["habr"] == 1
            assert element["content_count"]["vc"] == 1
            assert element["content_count"]["youtube"] == 1
            assert element["content_count"]["telegram"] == 1
            assert element["content_count"]["linkedin"] == 1
            assert element["content_count"]["instagram"] == 1
            assert element["content_count"]["other"] == 1

            assert "last_update" in element

    url = "api/v1/content"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 5
    assert_instances(response.json())


@pytest.mark.django_db
def test_ambassador_content(client: APIClient, create_content):
    def assert_instance(instance):
        assert instance["id"] == 1
        assert "user_pic" in instance
        assert instance["status"] == "active"
        assert instance["first_name"] == "Иван1"
        assert instance["last_name"] == "Иванов1"
        assert instance["tg_acc"] == "ivanov1"
        assert instance["email"] == "ivan.ivanov1@example.com"
        assert instance["phone"] == "7 (917) 123-45-61"
        assert instance["ya_programm_name"] == "Programm1"
        assert instance["city_address"] == "Город1"

        assert isinstance(instance["content"], list)
        for element in instance["content"]:
            assert "id" in element
            assert "created" in element
            assert "link" in element
            assert "files" in element

    url = "api/v1/ambassadors/1/content"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["content"]) == 8
    assert_instance(response.json())


@pytest.mark.django_db
def test_single_content(client: APIClient, create_content):
    url = "api/v1/ambassadors/1/content/1"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == 1
    assert "user_pic" in data
    assert data["status"] == "active"
    assert data["first_name"] == "Иван1"
    assert data["last_name"] == "Иванов1"
    assert data["tg_acc"] == "ivanov1"
    assert data["email"] == "ivan.ivanov1@example.com"
    assert data["phone"] == "7 (917) 123-45-61"
    assert data["ya_programm_name"] == "Programm1"
    assert data["city_address"] == "Город1"

    assert data["link"] == "https://youtube.com"
    assert data["files"] is None
    assert data["service"] == "youtube"
    assert data["status"] == "accepted"
    assert "created" in data


@pytest.mark.django_db
def test_all_promocodes(client: APIClient, create_promocodes):
    def assert_instances(instances):
        for element, index in enumerate(instances):
            assert element["id"] == 5 - index
            assert "user_pic" in element
            assert element["status"] == "active"
            assert element["first_name"] == f"Иван{5 - index}"
            assert element["last_name"] == f"Иванов{5 - index}"
            assert element["ya_programm_name"] == f"Programm{5 - index}"
            assert element["tg_acc"] == f"ivanov{5 - index}"
            assert element["promocode"]["name"] == f"promocode{5 - index}"
            assert "created" in element["promocode"]

    url = "api/v1/promocodes"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert_instances(response.json())
