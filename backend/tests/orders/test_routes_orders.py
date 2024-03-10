from http import HTTPStatus

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_track_orders(client: APIClient, create_orders):
    def assert_instances(instances):
        for index, element in enumerate(instances):
            assert element["id"] == 5 - index
            assert "image" in element["ambassador"]
            assert element["ambassador"]["status"] == "Active"
            assert element["ambassador"]["first_name"] == f"Иван{5 - index}"
            assert element["ambassador"]["last_name"] == f"Иванов{5 - index}"
            assert (
                element["ambassador"]["ya_programm"] == f"Programm{5 - index}"
            )
            assert element["ambassador"]["tg_acc"] == f"ivanov{5 - index}"
            assert element["track_number"] == f"track_number{5 - index}"
            assert "created_date" in element
            assert "status" in element

    url = "/api/v1/orders/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert_instances(response.json())


@pytest.mark.django_db
def test_single_order(client: APIClient, create_orders):
    def assert_instance(instance):
        assert instance["id"] == 1
        assert instance["first_name"] == "Имя"
        assert instance["last_name"] == "Фамилия"
        assert instance["middle_name"] == "Отчество"
        assert instance["phone"] == "7(917)123-45-61"

        assert instance["country"] == "Страна"
        assert instance["city"] == "Город"
        assert instance["street_home"] == "УлицаДом"
        assert instance["post_index"] == 123456

        assert isinstance(instance["merch"], list)
        for e in instance["merch"]:
            assert "name" in e
            assert "size" in e

    url = "/api/v1/orders/1/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert_instance(response.json())


@pytest.mark.django_db
def test_all_orders(client: APIClient, create_orders):
    def assert_instances(instances):
        for index, element in enumerate(instances):
            assert element["id"] == 5 - index
            assert "image" in element["ambassador"]
            assert element["ambassador"]["tg_acc"] == f"ivanov{5 - index}"
            assert isinstance(element["merch"], list[dict])
            for type in element["merch"]:
                assert "name" in type
                assert "count" in type
            assert "total_cost" in element
            assert "last_delivered" in element

    url = "/api/v1/merch_to_ambassador/"
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert_instances(response.json())


@pytest.mark.django_db
def test_ambassador_orders(client: APIClient, create_orders):
    def assert_instance(instance):
        assert "id" in instance
        assert "image" in instance
        assert "first_name" in instance
        assert "last_name" in instance
        assert "middle_name" in instance
        assert "city" in instance
        assert "ya_programm" in instance
        assert "phone" in instance
        assert "email" in instance
        assert "tg_acc" in instance
        assert isinstance(instance["merch"], list)

        for single_merch in instance["merch"]:
            assert "delivered_date" in single_merch
            assert "total_cost" in single_merch
            assert "name" in single_merch
            assert "size" in single_merch
            assert "amount" in single_merch

    url = "/api/v1/ambassadors/1/orders/"
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert_instance(response.json())
