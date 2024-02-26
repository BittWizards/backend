from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from ambassadors.models import Ambassador
from ambassadors_project import settings


class Platform(models.TextChoices):
    """Варианты платформ для размещения"""

    REVIEW = ("review", "Отзыв")
    HABR = ("habr", "Хабр")
    VC = ("VC", "VC")
    YOUTUBE = ("youtube", "youtube")
    TG = ("telegram", "телеграм")
    PHOTO_IN_MERCH = ("photo", "фото в мерче")
    INSTAGRAM = ("instagram", "инстаграм")
    LINKEDIN = ("linkedin", "linkedin")
    PROJECT = ("project", "участие в проекте")


class Content(models.Model):
    """Таблица для хранения контента"""

    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        verbose_name="Амбассадор",
        related_name="my_content",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата отчета", auto_now_add=True, db_index=True
    )
    link = models.URLField(verbose_name="ссылка на контент")
    start_guid = models.BooleanField(default=False, verbose_name="По гайду")
    platform = models.CharField(
        max_length=max([len(platform) for platform in Platform]),
        choices=Platform.choices,
        verbose_name="Площадка",
    )
    comment = models.TextField(verbose_name="комментарий менеджера")
    accepted = models.BooleanField(
        default=False, verbose_name="Заявка принята"
    )

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"
        ordering = ("-created_at", "ambassador")

    def __str__(self):
        return self.platform


class Screenshots(models.Model):
    """Таблица для хранения скриншотов к отчетам о контентах"""

    content = models.ForeignKey(
        Content,
        verbose_name="скриншоты",
        related_name="screen",
        on_delete=models.CASCADE,
    )
    screen = models.URLField(
        verbose_name="Скриншот",
    )

    class Meta:
        verbose_name = "Скриншот"
        verbose_name_plural = "скришоты"
        ordering = ("content",)

    def __str__(self):
        return self.screen


class Promocode(models.Model):
    """
    Таблица промокодов
    """

    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        verbose_name="Амбассадор",
        related_name="my_promocode",
    )
    promocode = models.CharField(
        max_length=settings.PROMOSIZE,
        verbose_name="промокод",
        validators=[
            RegexValidator(
                regex="[А-ЯA-Z0-9]+",
                message="Промокод должен состоять из заглавных букв и цифр",
            )
        ],
    )
    is_active = models.BooleanField(default=True, verbose_name="активный")
    created_at = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
        ordering = ("-created_at",)

    def __str__(self):
        return self.promocode

    def clean(self):
        super().clean()
        if self.is_active:
            if Promocode.objects.filter(
                ambassador=self.ambassador, is_active=True
            ).exclude(pk=self.pk):
                raise ValidationError("У амбассадора есть активный промокод'")
