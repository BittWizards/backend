from http import HTTPStatus

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_all_content(client: APIClient, create_content):
    def assert_instances(instances):
        for index, element in enumerate(instances):
            assert element["id"] == create_content[index]
            assert element["image"] == (
                "http://testserver/media/profiles/default_pic.jpeg"
            )
            assert element["first_name"] == f"Иван{index + 1}"
            assert element["last_name"] == f"Иванов{index + 1}"
            assert element["tg_acc"] == f"ivanov{index + 1}"
            assert "rating" in element

            assert element["review_count"] == 1
            assert element["habr_count"] == 1
            assert element["vc_count"] is None
            assert element["youtube_count"] is None
            assert element["tg_count"] is None
            assert element["linkedin_count"] is None
            assert element["instagram_count"] is None
            assert element["other_count"] is None

            assert "last_created" in element

    url = "/api/v1/allcontent/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 5
    assert_instances(response.json())


@pytest.mark.django_db
def test_ambassador_content(client: APIClient, create_content):
    def assert_instance(instance):
        assert instance["id"] == 1
        assert "image" in instance
        assert instance["accepted"] is True
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
            assert "created_at" in element
            assert "link" in element
            assert "files" in element

    url = "/api/v1/ambassadors/1/content/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    # assert len(response.json()["content"]) == 8
    assert_instance(response.json())


@pytest.mark.django_db
def test_single_content(client: APIClient, create_content):
    url = f"/api/v1/content/{create_content[0]}/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == create_content[0]
    assert "image" in data["ambassador"]
    assert data["ambassador"]["status"] == "Active"
    assert data["ambassador"]["first_name"] == "Иван1"
    assert data["ambassador"]["last_name"] == "Иванов1"
    assert data["ambassador"]["tg_acc"] == "ivanov1"
    assert data["ambassador"]["email"] == "ivan.ivanov1@example.com"
    assert data["ambassador"]["phone"] == "7(917)123-45-61"
    assert data["ambassador"]["ya_programm"] == "Programm1"
    assert data["ambassador"]["city"] == "Город1"

    assert data["link"] == "http://localhost/1"
    # assert data["files"] is None
    assert data["accepted"] is True
    assert "created_at" in data


@pytest.mark.django_db
def test_all_promocodes(client: APIClient, create_promocodes):
    def assert_instances(instances):
        for index, element in enumerate(instances):
            assert element["is_active"] is True
            assert "image" in element["ambassador"]
            assert element["ambassador"]["status"] == "Active"
            assert element["ambassador"]["first_name"] == f"Иван{5 - index}"
            assert element["ambassador"]["last_name"] == f"Иванов{5 - index}"
            assert (
                element["ambassador"]["ya_programm"] == f"Programm{5 - index}"
            )
            assert element["ambassador"]["tg_acc"] == f"ivanov{5 - index}"
            assert element["promocode"] == f"PROMO{5 - index}"
            assert "created_at" in element

    url = "/api/v1/promocodes/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert_instances(response.json())
