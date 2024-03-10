from ambassadors.choices import Achievement
from ambassadors.models import Ambassador
from ambassadors_project.constants import (
    CONTENT_COUNT_FOR_ACHIEV,
    NEW_ACHIEV_MESSAGE,
    REVIEW_COUNT_FOR_ACHIEV,
)
from content.models import Content, ContentType
from mailing.utils import send_to_ambassadors_email, send_to_ambassadors_tg
from orders.models import Order


def change_achievement_create_order(
    ambassador: Ambassador, new_achievement
) -> None:
    ambassador.achievement = new_achievement
    ambassador.save()
    Order.objects.create(ambassador=ambassador)
    send_to_ambassadors_email(
        ambassador, "Новое достижение!", NEW_ACHIEV_MESSAGE
    )
    send_to_ambassadors_tg(ambassador, NEW_ACHIEV_MESSAGE)


def add_achievments(ambassador: Ambassador) -> None:
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
