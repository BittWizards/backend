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
    assert response.status == HTTPStatus.OK
    assert len(response.json()) == 5
    assert_instances(response.json())
