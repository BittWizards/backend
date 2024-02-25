# flake8: noqa
import datetime as dt

import pytest
from ambassadors.models import (Actions, Ambassador, AmbassadorAddress,
                                AmbassadorsActions, AmbassadorSize,
                                YandexProgramm)
from content.models import Content, Promocode
from merch.models import Merch


@pytest.fixture
def create_ambassadors():
    now = dt.datetime.utcnow()
    programms = [
        YandexProgramm.objects.create(title=f"Programm{i}", description=f"{i}")
        for i in range(1, 6)
    ]
    actions = [
        Actions.objects.create(title=f"Actions{i}", description=f"{i}")
        for i in range(1, 7)
    ]
    for i in range(1, 6):
        ambassador = Ambassador.objects.create(
            email=f"ivan.ivanov{i}@example.com",
            first_name=f"Иван{i}",
            last_name=f"Иванов{i}",
            middle_name=f"Иванович{i}",
            gender="male",
            ya_programm=programms[i],
            phone=f"7 (917) 123-45-6{i}",
            tg_acc=f"ivanov{i}",
            goal="Закончить",
            education="9 классов",
            work_now="Беллинсгаузен",
            status="active",
            created=now,
        )

        AmbassadorsActions.objects.create(
            ambassador_id=ambassador,
            action=actions[i],
        )
        AmbassadorsActions.objects.create(
            ambassador_id=ambassador,
            action=actions[i + 1],
        )
        AmbassadorAddress.objects.create(
            country="Страна",
            city=f"Город{i}",
            street_home=f"Улица{i}",
            post_index=f"10000{i}",
            ambassador_id=ambassador,
        )
        AmbassadorSize.objects.create(
            ambassador_id=ambassador,
            clothes_size="M",
            foot_size="35-39",
        )


@pytest.fixture
def create_content(create_ambassadors):
    ...


@pytest.fixture
def create_merch():
    Merch.objects.create(
        type="Толстовка",
        price=100,
    )
    Merch.objecrs.create(
        type="plus",
        price=0,
    )
    Merch.objecrs.create(
        type="backpack",
        price=200,
    )
