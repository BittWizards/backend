from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from ambassadors.models import Ambassador
from ambassadors_project.constants import (
    ERROR_MESSAGE_PROMOCODE,
    PATTERN_PROMO,
    PROMOSIZE,
)


class Platform(models.TextChoices):
    """Варианты платформ для размещения"""

    HABR = ("habr", "Хабр")
    VC = ("VC", "VC")
    YOUTUBE = ("youtube", "Youtube")
    TG = ("telegram", "Телеграм")
    INSTAGRAM = ("instagram", "Инстаграм")
    LINKEDIN = ("linkedin", "lLinkedin")
    OTHER = ("other", "Прочее")


class ContentType(models.TextChoices):
    """Тип контента"""

    REVIEW = ("review", "Отзыв")
    CONTENT = ("content", "Контент")
    PHOTO = ("photo", "Фото с мерчем")


class Content(models.Model):
    """Таблица для хранения контента"""

    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        verbose_name="Амбассадор",
        related_name="my_content",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата отчета", default=timezone.now, db_index=True
    )
    link = models.URLField(verbose_name="ссылка на контент", unique=True)
    start_guide = models.BooleanField(default=False, verbose_name="По гайду")
    type = models.CharField(
        null=True,
        blank=True,
        choices=ContentType.choices,
        verbose_name="Тип контента",
    )
    platform = models.CharField(
        max_length=max([len(platform) for platform in Platform]),
        null=True,
        blank=True,
        choices=Platform.choices,
        verbose_name="Площадка",
    )
    comment = models.TextField(
        null=True, blank=True, verbose_name="комментарий менеджера"
    )
    accepted = models.BooleanField(
        default=False, verbose_name="Заявка принята"
    )

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"
        ordering = ("-created_at", "ambassador")

    def __str__(self) -> str:
        return f"content_id: {self.pk}"


class Documents(models.Model):
    """Таблица для хранения скриншотов к отчетам о контентах"""

    content = models.ForeignKey(
        Content,
        verbose_name="Контент_id",
        related_name="documents",
        on_delete=models.CASCADE,
    )
    document = models.URLField(
        max_length=400,
        verbose_name="Ссылка на документ",
    )

    class Meta:
        verbose_name = "Доп.документ"
        verbose_name_plural = "Доп.документы"
        ordering = ("content",)

    def __str__(self) -> str:
        return self.document


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
        max_length=PROMOSIZE,
        verbose_name="промокод",
        validators=[
            RegexValidator(
                regex=PATTERN_PROMO,
                message=ERROR_MESSAGE_PROMOCODE,
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

    def __str__(self) -> str:
        return self.promocode

    def clean(self):
        super().clean()
        if self.is_active:
            if Promocode.objects.filter(
                ambassador=self.ambassador, is_active=True
            ).exclude(pk=self.pk):
                raise ValidationError("У амбассадора есть активный промокод'")
