from ambassadors.choices import Achievement
from ambassadors_project.constants import (
    CONTENT_COUNT_FOR_ACHIEV,
    REVIEW_COUNT_FOR_ACHIEV,
)
from content.models import Content, ContentType
from orders.models import Order


def change_achievement_create_order(ambassador, new_achievement):
    ambassador.achievement = new_achievement
    ambassador.save()
    Order.objects.create(ambassador=ambassador)
    # TODO отправить сообщение


def add_achievments(ambassador):
    if ambassador.achievement == Achievement.NEW:
        if (
            Content.objects.filter(
                ambassador=ambassador, type=ContentType.REVIEW, accepted=True
            ).count()
            == REVIEW_COUNT_FOR_ACHIEV
        ):
            change_achievement_create_order(ambassador, Achievement.FRIEND)
    elif ambassador.achievement == Achievement.FRIEND:
        if (
            Content.objects.filter(
                ambassador=ambassador, type=ContentType.CONTENT, accepted=True
            ).count()
            == CONTENT_COUNT_FOR_ACHIEV
        ):
            change_achievement_create_order(
                ambassador, Achievement.PROFI_FRIEND
            )
