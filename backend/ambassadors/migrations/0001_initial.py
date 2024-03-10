# Generated by Django 4.2.9 on 2024-03-09 09:53

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Actions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=150, verbose_name="Заголовок"),
                ),
                (
                    "description",
                    models.CharField(max_length=2000, verbose_name="Описание"),
                ),
            ],
            options={
                "verbose_name": "Действие",
                "verbose_name_plural": "Действия",
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="Ambassador",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=100, verbose_name="Имя"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=100, verbose_name="Фамилия"),
                ),
                (
                    "middle_name",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="Отчество"
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=15, verbose_name="Номер телефона"
                    ),
                ),
                (
                    "email",
                    models.CharField(
                        max_length=200,
                        unique=True,
                        verbose_name="Электронная почта",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("Male", "Мужчина"), ("Female", "Женщина")],
                        max_length=20,
                        verbose_name="Пол",
                    ),
                ),
                (
                    "purpose",
                    models.CharField(
                        blank=True,
                        max_length=300,
                        null=True,
                        verbose_name="цель обучения",
                    ),
                ),
                (
                    "education",
                    models.CharField(
                        max_length=300, verbose_name="Образование"
                    ),
                ),
                (
                    "work",
                    models.CharField(
                        blank=True, null=True, verbose_name="Работа"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Active", "Активный"),
                            ("Pause", "На паузе"),
                            ("Clarify", "Уточняется"),
                            ("Not active", "Не активный"),
                        ],
                        default="Clarify",
                        max_length=50,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Дата и время создания",
                    ),
                ),
                (
                    "tg_acc",
                    models.CharField(
                        max_length=150,
                        unique=True,
                        verbose_name="Телеграмм аккаунт",
                    ),
                ),
                (
                    "tg_id",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Телеграмм id"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        default="profiles/default_pic.jpeg",
                        null=True,
                        upload_to="profiles/",
                        verbose_name="Фото",
                    ),
                ),
                (
                    "achievement",
                    models.CharField(
                        choices=[
                            ("new", "Новичок"),
                            ("friend", "Друг практикума"),
                            ("profi_friend", "Практикующий амбассадор"),
                        ],
                        default="new",
                        verbose_name="Ачивка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Амбассадор",
                "verbose_name_plural": "Амбассадоры",
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="YandexProgramm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=300, verbose_name="заголовок"),
                ),
                (
                    "description",
                    models.CharField(max_length=1000, verbose_name="Описание"),
                ),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="AmbassadorSize",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "clothes_size",
                    models.CharField(
                        choices=[
                            ("XS", "XS"),
                            ("S", "S"),
                            ("M", "M"),
                            ("L", "L"),
                            ("XL", "XL"),
                        ],
                        max_length=30,
                        verbose_name="Размер одежды",
                    ),
                ),
                (
                    "foot_size",
                    models.CharField(
                        choices=[
                            ("35", "35"),
                            ("36", "36"),
                            ("37", "37"),
                            ("38", "38"),
                            ("39", "39"),
                            ("40", "40"),
                            ("41", "41"),
                            ("42", "42"),
                            ("43", "43"),
                            ("44", "44"),
                            ("45", "45"),
                        ],
                        verbose_name="Размер обуви",
                    ),
                ),
                (
                    "ambassador_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="size",
                        to="ambassadors.ambassador",
                        verbose_name="Амбассадор",
                    ),
                ),
            ],
            options={
                "verbose_name": "Размеры амбассадора",
                "verbose_name_plural": "Размеры амбассадоров",
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="AmbassadorAddress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "country",
                    models.CharField(max_length=100, verbose_name="Страна"),
                ),
                (
                    "city",
                    models.CharField(max_length=100, verbose_name="Город"),
                ),
                (
                    "street_home",
                    models.CharField(max_length=200, verbose_name="Улица"),
                ),
                ("post_index", models.IntegerField(verbose_name="Индекс")),
                (
                    "ambassador_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="address",
                        to="ambassadors.ambassador",
                        verbose_name="Амбассадор",
                    ),
                ),
            ],
            options={
                "verbose_name": "Адрес амбассадора",
                "verbose_name_plural": "Адреса амбассадоров",
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="AmbassadorActions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "action",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="ambassadors.actions",
                        verbose_name="Действие",
                    ),
                ),
                (
                    "ambassador_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="actions",
                        to="ambassadors.ambassador",
                        verbose_name="Амбассадор",
                    ),
                ),
            ],
            options={
                "verbose_name": "Действие амбассадора",
                "verbose_name_plural": "Действия амбассадоров",
                "ordering": ("id",),
            },
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
