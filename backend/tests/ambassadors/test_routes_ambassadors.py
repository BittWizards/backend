from http import HTTPStatus

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_get_ambassadors(client: APIClient, create_ambassadors):
    def assert_instances(instances):
        for element, index in enumerate(instances):
            assert element["id"] == index + 1
            assert element["email"] == f"ivan.ivanov{index}@example.com"
            assert element["first_name"] == f"Иван{index}"
            assert element["last_name"] == f"Иванов{index}"
            assert element["middle_name"] == f"Иванович{index}"
            assert element["gender"] == "male"
            assert element["phone"] == f"7 (917) 123-45-6{index}"
            assert element["tg_acc"] == f"ivanov{index}"
            assert element["education"] == "9 классов"
            assert element["work_now"] is True
            assert element["status"] == "active"
            assert element["education"] == "9 классов"
            assert element["education"] == "9 классов"

            assert isinstance(element["ya_programm"], dict)
            assert isinstance(element["ambassador_actions"], list[dict])
            assert isinstance(element["address"], dict)
            assert isinstance(element["sizes"], dict)

    url = ""
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5
    assert_instances(response.json())
