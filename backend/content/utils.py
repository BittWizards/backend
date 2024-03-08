from ambassadors.choices import Achievement
from ambassadors_project.constants import (
    CONTENT_COUNT_FOR_ACHIEV,
    REVIEW_COUNT_FOR_ACHIEV,
)
from content.models import Content, ContentType
from orders.models import Order


def add_achievments(ambassador):
    if ambassador.achievement == Achievement.NEW:
        if (
            Content.objects.filter(
                ambassador=ambassador, type=ContentType.REVIEW, accepted=True
            ).count()
            == REVIEW_COUNT_FOR_ACHIEV
        ):
            ambassador.achievement = Achievement.FRIEND
            ambassador.save()
            Order.objects.create(ambassador=ambassador)
        # TODO отправить сообщение
    elif ambassador.achievement == Achievement.FRIEND:
        if (
            Content.objects.filter(
                ambassador=ambassador, type=ContentType.CONTENT, accepted=True
            ).count()
            == CONTENT_COUNT_FOR_ACHIEV
        ):
            ambassador.achievement = Achievement.PROFI_FRIEND
            ambassador.save()
            Order.objects.create(ambassador=ambassador)
    # TODO отправить сообщение
