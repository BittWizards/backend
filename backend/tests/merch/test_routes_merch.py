from http import HTTPStatus

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_track_merch(client: APIClient, create_merch):
    def assert_instances(instances):
        for element, index in enumerate(instances):
            assert element["id"] == 5 - index
            assert "user_pic" in element
            assert element["status"] == "active"
            assert element["first_name"] == f"Иван{5 - index}"
            assert element["last_name"] == f"Иванов{5 - index}"
            assert element["ya_programm_name"] == f"Programm{5 - index}"
            assert element["tg_acc"] == f"ivanov{5 - index}"
            assert (
                element["merch"]["track_number"] == f"track_number{5 - index}"
            )
            assert "created" in element["merch"]

    url = "api/v1/merch/track"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert_instances(response.json())


@pytest.mark.django_db
def test_single_merch(client: APIClient, create_merch):
    def assert_instance(instance):
        assert instance["id"] == 1
        assert "user_pic" in instance
        assert instance["first_name"] == "Иван1"
        assert instance["last_name"] == "Иванов1"
        assert instance["middle_name"] == "Иванович1"
        assert instance["gender"] == "male"
        assert instance["tg_acc"] == "ivanov1"
        assert instance["email"] == "ivan.ivanov1@example.com"
        assert instance["phone"] == "7 (917) 123-45-61"

        assert isinstance(instance["address"], dict)
        assert instance["address"]["country"] == "Страна"
        assert instance["address"]["city"] == "Город1"
        assert instance["address"]["street_home"] == "Улица1"
        assert instance["address"]["post_index"] == "100001"

        assert isinstance(instance["sizes"], dict)
        assert instance["size"]["clothes_size"] == "M"
        assert instance["size"]["foot_size"] == "35-39"

        assert isinstance(instance["merch_type"], list)

    url = "api/v1/merch/1"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert_instance(response.json())


@pytest.mark.django_db
def test_all_merch(client: APIClient, create_merch):
    def assert_instances(instances):
        for element, index in enumerate(instances):
            assert element["id"] == 5 - index
            assert "user_pic" in element
            assert element["tg_acc"] == f"ivanov{5 - index}"
            assert isinstance(element["merch"], list[dict])
            for type in element["merch"]:
                assert "type" in type
                assert type["coount"] == 1
            assert "summ" in element

    url = "api/v1/merch"
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert_instances(response.json())
