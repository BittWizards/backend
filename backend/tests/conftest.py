# flake8: noqa
import time

import pytest
from django.conf import settings
from django.db.models import signals

from ambassadors.models import (
    Actions,
    Ambassador,
    AmbassadorActions,
    AmbassadorAddress,
    AmbassadorSize,
    YandexProgramm,
)
from content.models import Content, Documents, Promocode
from orders.models import Merch, Order


@pytest.fixture(scope="session", autouse=True)
def disable_signals():
    signals.post_save.disconnect()
    settings.CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }


@pytest.fixture
def create_ambassadors(db):
    programms = [
        YandexProgramm.objects.create(
            id=i, title=f"Programm{i}", description=f"{i}"
        )
        for i in range(1, 6)
    ]
    actions = [
        Actions.objects.create(id=i, title=f"Actions{i}", description=f"{i}")
        for i in range(1, 7)
    ]
    ambassadors = []
    for i in range(1, 6):
        ambassador = Ambassador.objects.create(
            id=i,
            email=f"ivan.ivanov{i}@example.com",
            first_name=f"Иван{i}",
            last_name=f"Иванов{i}",
            middle_name=f"Иванович{i}",
            gender="Male",
            ya_programm=programms[i - 1],
            phone=f"7(917)123-45-6{i}",
            tg_acc=f"ivanov{i}",
            purpose="Закончить",
            education="9 классов",
            work="Беллинсгаузен",
            status="Active",
        )

        AmbassadorActions.objects.create(
            ambassador=ambassador,
            action=actions[i - 1],
        )
        AmbassadorAddress.objects.create(
            ambassador=ambassador,
            country="Страна",
            city=f"Город{i}",
            street_home=f"Улица{i}",
            post_index=f"10000{i}",
        )
        AmbassadorSize.objects.create(
            ambassador=ambassador,
            clothes_size="M",
            foot_size="37",
        )
        ambassadors.append(ambassador)
    return ambassadors


@pytest.fixture
def create_new_ambassadors(create_ambassadors):
    for i in range(1, 3):
        ambassador = Ambassador.objects.create(
            id=5 + i,
            email=f"ivan.ivanov{5 + i}@example.com",
            first_name=f"Иван{5 + i}",
            last_name=f"Иванов{5 + i}",
            middle_name=f"Иванович{5 + i}",
            gender="Male",
            ya_programm_id=i,
            phone=f"7(917)123-45-6{5 + i}",
            tg_acc=f"ivanov{5 + i}",
            purpose="Закончить",
            education="9 классов",
            work="Беллинсгаузен",
            status="Clarify",
        )


@pytest.fixture
def create_content(create_ambassadors):
    ids = []
    for i in range(1, 6):
        content1 = Content.objects.create(
            ambassador_id=i,
            link=f"http://localhost/{i}",
            accepted=True,
            type="review",
        )
        ids.append(content1.id)
        content2 = Content.objects.create(
            ambassador_id=i,
            link=f"http://localhost/2{i}",
            accepted=True,
            type="content",
            platform="habr",
        )
        ids.append(content2.id)
        Documents.objects.create(
            content=content1,
            document=f"http://localhost:1/d{i}.jpg",
        )
        Documents.objects.create(
            content=content2,
            document=f"http://localhost:2/d2{i}.png",
        )
    return ids


@pytest.fixture
def create_promocodes(create_ambassadors):
    for i in range(1, 6):
        Promocode.objects.create(
            ambassador_id=i,
            promocode=f"PROMO{i}",
        )
        time.sleep(0.1)


@pytest.fixture
def create_merch():
    hoodie = Merch.objects.create(
        name="Толстовка",
        size="XL",
    )
    plus = Merch.objects.create(
        name="plus",
    )
    socks = Merch.objects.create(
        name="Носки",
        size=37,
    )
    return (hoodie, plus, socks)


@pytest.fixture
def create_orders(create_ambassadors, create_merch):
    for i in range(1, 6):
        order = Order.objects.create(
            id=i,
            ambassador_id=i,
            phone=f"7(917)123-45-6{i}",
            first_name="Имя",
            last_name="Фамилия",
            middle_name="Отчество",
            country="Страна",
            city="Город",
            street_home="УлицаДом",
            post_index=123456,
            track_number=f"track_number{i}",
        )
        order.merch.set(create_merch)
        time.sleep(0.1)
