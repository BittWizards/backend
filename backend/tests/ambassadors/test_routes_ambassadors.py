from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

# @pytest.mark.django_db
# def test_get_ambassadors(client: APIClient, create_ambassadors):
#     def assert_instances(instances):
#         for element, index in enumerate(instances):
#             assert element["id"] == index + 1
#             assert element["email"] == f"ivan.ivanov{index + 1}@example.com"
#             assert element["first_name"] == f"Иван{index + 1}"
#             assert element["last_name"] == f"Иванов{index + 1}"
#             assert element["middle_name"] == f"Иванович{index + 1}"
#             assert element["gender"] == "male"
#             assert element["phone"] == f"7 (917) 123-45-6{index + 1}"
#             assert element["tg_acc"] == f"ivanov{index + 1}"
#             assert element["education"] == "9 классов"
#             assert element["work_now"] is True
#             assert element["status"] == "active"

#             assert isinstance(element["ya_programm"], dict)
#             assert isinstance(element["ambassador_actions"], list[dict])
#             assert isinstance(element["address"], dict)
#             assert isinstance(element["sizes"], dict)

#     url = ""
#     response = client.get(url)
#     assert response.status_code == HTTPStatus.OK
#     assert isinstance(response.json(), list)
#     assert len(response.json()) == 5
#     assert_instances(response.json())


@pytest.mark.django_db
def test_all_ambassadors(client: APIClient, create_ambassadors):
    def assert_instances(instances):
        for element, index in enumerate(instances):
            assert element["id"] == index + 1
            assert "user_pic" in element
            assert element["first_name"] == f"Иван{index + 1}"
            assert element["last_name"] == f"Иванов{index + 1}"
            assert element["middle_name"] == f"Иванович{index + 1}"
            assert element["status"] == "active"
            assert element["ya_programm_name"] == f"Programm{index + 1}"
            assert element["phone"] == f"7 (917) 123-45-6{index + 1}"
            assert element["tg_acc"] == f"ivanov{index + 1}"
            assert "created" in element

    url = "api/v1/ambassadors"
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5
    assert_instances(response.json())


@pytest.mark.django_db
def test_new_ambassadors(client: APIClient, create_new_ambassadors):
    def assert_instances(instances):
        for element, index in enumerate(instances):
            assert element["id"] == index + 1
            assert "user_pic" in element
            assert element["first_name"] == f"Иван{index + 1}"
            assert element["last_name"] == f"Иванов{index + 1}"
            assert element["middle_name"] == f"Иванович{index + 1}"
            assert element["ya_programm_name"] == f"Programm{index + 1}"
            assert "created" in element

    url = "api/v1/ambassadors/new"
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5
    assert_instances(response.json())


@pytest.mark.django_db
def test_ambassador_profile(client: APIClient, create_ambassadors):
    def assert_instance(instance):
        assert instance["id"] == 1
        assert "user_pic" in instance
        assert instance["status"] == "active"

        assert instance["first_name"] == "Иван1"
        assert instance["last_name"] == "Иванов1"
        assert instance["middle_name"] == "Иванович1"
        assert instance["gender"] == "male"

        assert instance["email"] == "ivan.ivanov1@example.com"
        assert instance["phone"] == "7 (917) 123-45-61"
        assert instance["tg_acc"] == "ivanov1"

        assert isinstance(instance["address"], dict)
        assert instance["address"]["country"] == "Страна"
        assert instance["address"]["city"] == "Город1"
        assert instance["address"]["street_home"] == "Улица1"
        assert instance["address"]["post_index"] == "100001"

        assert isinstance(instance["sizes"], dict)
        assert instance["size"]["clothes_size"] == "M"
        assert instance["size"]["foot_size"] == "35-39"

        assert isinstance(instance["ya_programm"], dict)
        assert instance["goal"] == "Закончить"
        assert instance["work"] == "Беллинсгаузен"
        assert instance["education"] == "9 классов"

        assert isinstance(instance["ambassador_actions"], list[dict])

        assert instance["extra_info"] == "Хороший человек"

    url = "api/v1/ambassadors/1"
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert_instance(response.json())
