from http import HTTPStatus

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_track_merch(client: APIClient, create_orders):
    def assert_instances(instances):
        for index, element in enumerate(instances):
            assert element["id"] == 5 - index
            assert "image" in element
            assert element["status"] == "active"
            assert element["first_name"] == f"Иван{5 - index}"
            assert element["last_name"] == f"Иванов{5 - index}"
            assert element["ya_programm_name"] == f"Programm{5 - index}"
            assert element["tg_acc"] == f"ivanov{5 - index}"
            assert (
                element["merch"]["track_number"] == f"track_number{5 - index}"
            )
            assert "created" in element["merch"]
            assert "status" in element["merch"]

    url = "/api/v1/orders/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert_instances(response.json())


@pytest.mark.django_db
def test_single_merch(client: APIClient, create_orders):
    def assert_instance(instance):
        assert instance["id"] == 1
        assert "image" in instance
        assert instance["first_name"] == "Иван1"
        assert instance["last_name"] == "Иванов1"
        assert instance["middle_name"] == "Иванович1"
        assert instance["phone"] == "7(917)123-45-61"

        assert instance["country"] == "Страна"
        assert instance["city"] == "Город1"
        assert instance["street_home"] == "Улица1"
        assert instance["post_index"] == "100001"

        # TODO
        # assert isinstance(instance["sizes"], dict)
        # assert instance["size"]["clothes_size"] == "M"
        # assert instance["size"]["foot_size"] == "35-39"

        assert isinstance(instance["merch"], list)

    url = "/api/v1/orders/1/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert_instance(response.json())


@pytest.mark.django_db
def test_all_merch(client: APIClient, create_orders):
    def assert_instances(instances):
        for index, element in enumerate(instances):
            assert element["id"] == 5 - index
            assert "image" in element
            assert element["tg_acc"] == f"ivanov{5 - index}"
            assert isinstance(element["merch"], list[dict])
            for type in element["merch"]:
                assert "name" in type
                assert "count" in type
            assert "total_cost" in element

    url = "/api/v1/merch_to_ambassador/"
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert_instances(response.json())
