from django.utils.timezone import make_aware

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


def import_ya_programms(self, obj):
    cells = obj.iter_rows()

    for id, title, description in cells:
        YandexProgramm.objects.get_or_create(
            id=id.value, title=title.value, description=description.value
        )

    self.stdout.write(self.style.SUCCESS("Яндекс курсы загружены"))


def import_actions(self, obj):
    cells = obj.iter_rows()

    for id, title, description in cells:
        Actions.objects.get_or_create(
            id=id.value, title=title.value, description=description.value
        )

    self.stdout.write(self.style.SUCCESS("Actions загружены"))


def import_ambassadors(self, obj):
    cells = obj.iter_rows()

    for (
        id,
        email,
        first_name,
        last_name,
        middle_name,
        phone,
        tg_acc,
        gender,
        ya_programm,
        purpose,
        education,
        work,
        status,
        created,
        image,
        achievement,
    ) in cells:
        Ambassador.objects.get_or_create(
            id=id.value,
            email=email.value,
            first_name=first_name.value,
            last_name=last_name.value,
            middle_name=middle_name.value,
            phone=phone.value,
            tg_acc=tg_acc.value,
            gender=gender.value,
            ya_programm_id=ya_programm.value,
            purpose=purpose.value,
            education=education.value,
            work=work.value,
            status=status.value,
            created=make_aware(created.value),
            image=image.value,
            achievement=achievement.value,
        )
    self.stdout.write(self.style.SUCCESS("Амбассадоры загружены"))


def import_address(self, obj):
    cells = obj.iter_rows()
    for country, city, street_home, post_index, ambassador_id in cells:
        AmbassadorAddress.objects.get_or_create(
            country=country.value,
            city=city.value,
            street_home=street_home.value,
            post_index=post_index.value,
            ambassador_id_id=ambassador_id.value,
        )
    self.stdout.write(self.style.SUCCESS("Адреса загружены"))


def import_ambass_actions(self, obj):
    cells = obj.iter_rows()

    for ambassador_id, action_id in cells:
        AmbassadorActions.objects.get_or_create(
            ambassador_id_id=ambassador_id.value, action_id=action_id.value
        )
    self.stdout.write(self.style.SUCCESS("Действия амбассадора загружены"))


def import_content(self, obj):
    cells = obj.iter_rows()

    for (
        id,
        ambassador_id,
        created_at,
        link,
        start_guide,
        type,
        platform,
        comment,
        accepted,
    ) in cells:
        Content.objects.get_or_create(
            id=id.value,
            ambassador_id=ambassador_id.value,
            created_at=created_at.value,
            link=link.value,
            start_guide=start_guide.value,
            type=type.value,
            platform=platform.value,
            comment=comment.value,
            accepted=accepted.value,
        )
    self.stdout.write(self.style.SUCCESS("Контент загружен"))


def import_docs(self, obj):
    cells = obj.iter_rows()

    for content_id, document in cells:
        Documents.objects.get_or_create(
            content_id=content_id.value, document=document.value
        )
    self.stdout.write(self.style.SUCCESS("Дополнительные файлы загружены"))


def import_sizes(self, obj):
    cells = obj.iter_rows()

    for ambassador_id, clothes_size, foot_size in cells:
        AmbassadorSize.objects.get_or_create(
            ambassador_id_id=ambassador_id.value,
            clothes_size=clothes_size.value,
            foot_size=foot_size.value,
        )
    self.stdout.write(self.style.SUCCESS("Размеры амбассадоров загружены"))


def import_promo(self, obj):
    cells = obj.iter_rows()

    for ambassador_id, promocode, is_active in cells:
        Promocode.objects.create(
            ambassador_id=ambassador_id.value,
            promocode=promocode.value,
            is_active=is_active.value,
        )
    self.stdout.write(self.style.SUCCESS("Промокоды амбассадоров загружены"))


def import_merch(self, obj):
    cells = obj.iter_rows()

    for merch_id, name, size in cells:
        Merch.objects.get_or_create(
            id=merch_id.value,
            name=name.value,
            size=size.value,
        )
    self.stdout.write(self.style.SUCCESS("Мерч загружен"))


def import_orders(self, obj):
    cells = obj.iter_rows()

    for (
        ambassador_id,
        first_name,
        last_name,
        middle_name,
        phone,
        country,
        city,
        street_home,
        post_index,
        merch_all,
        status,
        created_date,
        delivered_date,
        track_number,
        total_cost,
    ) in cells:
        order, created = Order.objects.get_or_create(
            ambassador_id=ambassador_id.value,
            first_name=first_name.value,
            last_name=last_name.value,
            middle_name=middle_name.value,
            phone=phone.value,
            country=country.value,
            city=city.value,
            street_home=street_home.value,
            post_index=post_index.value,
            status=status.value,
            created_date=created_date.value,
            delivered_date=delivered_date.value,
            track_number=track_number.value,
            total_cost=total_cost.value,
        )
        order.merch.set(str(merch_all.value).split(","))
    self.stdout.write(self.style.SUCCESS("Заказы загружены"))
