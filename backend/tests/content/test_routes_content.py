from http import HTTPStatus

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_all_content(client: APIClient, create_content):
    def assert_instances(instances):
        for index, element in enumerate(instances):
            print(element)
            assert element["id"] == index + 1
            assert element["image"] == (
                "http://testserver/media/profiles/default_pic.jpeg"
            )
            assert element["first_name"] == f"Иван{index + 1}"
            assert element["last_name"] == f"Иванов{index + 1}"
            assert element["tg_acc"] == f"ivanov{index + 1}"
            assert "rating" in element

            assert element["review_count"] == 1
            assert element["habr_count"] == 1
            assert element["vc_count"] == 1
            assert element["youtube_count"] == 1
            assert element["tg_count"] == 1
            assert element["linkedin_count"] == 1
            assert element["instagram_count"] == 1
            assert element["other_count"] == 1

            assert "last_update" in element

    url = "/api/v1/allcontents/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 5
    assert_instances(response.json())


@pytest.mark.django_db
def test_ambassador_content(client: APIClient, create_content):
    def assert_instance(instance):
        assert instance["id"] == 1
        assert "image" in instance
        assert instance["accepted"] == "True"
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

    url = "/api/v1/ambassadors/1/contents/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    # assert len(response.json()["content"]) == 8
    assert_instance(response.json())


@pytest.mark.django_db
def test_single_content(client: APIClient, create_content):
    url = "/api/v1/ambassadors/1/content/1/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == 1
    assert "image" in data
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
        for index, element in enumerate(instances):
            print(element)
            assert element["id"] == 5 - index
            assert "image" in element
            assert element["status"] == "Active"
            assert element["first_name"] == f"Иван{5 - index}"
            assert element["last_name"] == f"Иванов{5 - index}"
            assert element["ya_programm_name"] == f"Programm{5 - index}"
            assert element["tg_acc"] == f"ivanov{5 - index}"
            assert element["promocode"]["name"] == f"promocode{5 - index}"
            assert "created" in element["promocode"]

    url = "/api/v1/promocode/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert_instances(response.json())
