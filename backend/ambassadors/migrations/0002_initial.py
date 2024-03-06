# Generated by Django 4.2.9 on 2024-03-06 07:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ambassadors", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sendingmessage",
            name="supervisor_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Супервизор",
            ),
        ),
        migrations.AddField(
            model_name="messagetoambassador",
            name="ambassador_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="ambassadors.ambassador",
                verbose_name="Амбассадор",
            ),
        ),
        migrations.AddField(
            model_name="messagetoambassador",
            name="sending_message_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="ambassadors.sendingmessage",
                verbose_name="Сообщение",
            ),
        ),
        migrations.AddField(
            model_name="ambassadorsize",
            name="ambassador_id",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="size",
                to="ambassadors.ambassador",
                verbose_name="Амбассадор",
            ),
        ),
        migrations.AddField(
            model_name="ambassadoraddress",
            name="ambassador_id",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="address",
                to="ambassadors.ambassador",
                verbose_name="Амбассадор",
            ),
        ),
        migrations.AddField(
            model_name="ambassadoractions",
            name="action",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="ambassadors.actions",
                verbose_name="Действие",
            ),
        ),
        migrations.AddField(
            model_name="ambassadoractions",
            name="ambassador_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="actions",
                to="ambassadors.ambassador",
                verbose_name="Амбассадор",
            ),
        ),
        migrations.AddField(
            model_name="ambassador",
            name="ya_programm",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="ambassadors.yandexprogramm",
                verbose_name="Текущий курс",
            ),
        ),
    ]
