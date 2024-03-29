import re

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ambassadors.models import Ambassador, AmbassadorAddress
from ambassadors.serializers import ShortAmbassadorSerializer
from ambassadors.validators import tg_acc_validator
from ambassadors_project.constants import (
    ERROR_MESSAGE_PROMOCODE,
    ERROR_MESSAGE_SISE_PROMOCODE,
    PATTERN_PROMO,
    PROMOSIZE,
)
from content.models import Content, Documents, Promocode
from content.utils import add_achievments


class NewContentSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения заявок на контент."""

    ambassador = ShortAmbassadorSerializer(read_only=True)

    class Meta:
        model = Content
        fields = (
            "id",
            "ambassador",
            "created_at",
        )


class AllContentSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра всех пользователей с их контентом."""

    review_count = serializers.IntegerField(default=0)
    habr_count = serializers.IntegerField(default=0)
    rating = serializers.IntegerField(default=0)
    vc_count = serializers.IntegerField(default=0)
    youtube_count = serializers.IntegerField(default=0)
    tg_count = serializers.IntegerField(default=0)
    instagram_count = serializers.IntegerField(default=0)
    linkedin_count = serializers.IntegerField(default=0)
    other_count = serializers.IntegerField(default=0)
    last_date = serializers.DateTimeField()

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "image",
            "last_name",
            "first_name",
            "tg_acc",
            "status",
            "achievement",
            "rating",
            "review_count",
            "habr_count",
            "vc_count",
            "youtube_count",
            "tg_count",
            "instagram_count",
            "linkedin_count",
            "other_count",
            "last_date",
        )


class AmbassadorForContentPromoCardSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения данных амбассадора
     в карточках контента и промокодов.
    """

    city = serializers.SerializerMethodField()
    email = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    ya_programm = serializers.CharField(source="ya_programm.title")

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "image",
            "last_name",
            "first_name",
            "middle_name",
            "status",
            "achievement",
            "tg_acc",
            "email",
            "phone",
            "ya_programm",
            "city",
        )

    def get_city(self, obj: Ambassador) -> str:
        city = AmbassadorAddress.objects.get(ambassador_id=obj.id).city
        return city


class DocumentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ("document",)


class ContentSerializers(serializers.ModelSerializer):
    """Сериализатор для карточек контента."""

    ambassador = AmbassadorForContentPromoCardSerializer()
    id = serializers.IntegerField(required=False)
    documents = DocumentsSerializers(many=True, read_only=True)

    class Meta:
        model = Content
        fields = (
            "id",
            "created_at",
            "link",
            "start_guide",
            "type",
            "platform",
            "comment",
            "accepted",
            "ambassador",
            "documents",
        )


class PostContentSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и изменения контента."""

    name = serializers.CharField(required=False)
    tg_acc = serializers.CharField()
    files = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Content
        fields = (
            "link",
            "start_guide",
            "type",
            "platform",
            "comment",
            "accepted",
            "name",
            "tg_acc",
            "files",
        )

    def validate(self, data):
        if "tg_acc" in data:
            tg_acc_validator(data)
        if "files" in data:
            files = data.pop("files").split(", ")
            new_files = ""
            for file in files:
                if len(files) > 0:
                    if re.search(r"\w*$", file).group(0) in [
                        "png",
                        "jpg",
                        "jpeg",
                    ]:
                        new_files += file + ","
                        data["files"] = new_files
        return data

    def create(self, validated_data) -> Content:
        fio = validated_data.pop("name")  # noqa: F841
        tg_acc = validated_data.pop("tg_acc")
        files = None
        if "files" in validated_data:
            files = validated_data.pop("files").split(", ")
        ambassador = get_object_or_404(Ambassador, tg_acc=tg_acc)
        with transaction.atomic():
            content = Content.objects.get_or_create(
                **validated_data, ambassador=ambassador
            )[0]
            if files:
                docs_to_create = [
                    Documents(content=content, document=file) for file in files
                ]
                Documents.objects.bulk_create(docs_to_create)

        return content

    def update(self, instance: Content, validated_data: dict):
        super().update(instance, validated_data)
        if not validated_data.get("accepted"):
            return instance
        add_achievments(instance.ambassador)
        return instance

    def to_representation(self, instance: Content) -> dict:
        return ContentSerializers(
            instance, context={"request": self.context.get("request")}
        ).data


class PromocodeSerializer(serializers.ModelSerializer):
    """Сериализатор для промокодов."""

    ambassador = ShortAmbassadorSerializer(read_only=True)

    class Meta:
        model = Promocode
        fields = ("id", "promocode", "is_active", "created_at", "ambassador")


class PostPromocodeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания промокодов."""

    class Meta:
        model = Promocode
        fields = ("promocode", "ambassador")

    def deactivate(self, last_promo: list[Promocode]) -> None:
        for promocode in last_promo:
            promocode.is_active = False
            promocode.save()

    def create(self, validated_data: dict) -> Promocode:
        last_promo = Promocode.objects.filter(
            ambassador=validated_data["ambassador"], is_active=True
        )
        if last_promo:
            self.deactivate(last_promo)

        new_promo = Promocode.objects.create(**validated_data)
        return new_promo

    def validate(self, data: dict) -> dict:
        promocode = data.get("promocode")
        if not re.fullmatch(PATTERN_PROMO, promocode):
            raise ValidationError(ERROR_MESSAGE_PROMOCODE)
        if len(promocode) > PROMOSIZE:
            raise ValidationError(ERROR_MESSAGE_SISE_PROMOCODE)
        return data

    def to_representation(self, instance: Promocode) -> dict:
        return PromocodeSerializer(
            instance, context={"request": self.context.get("request")}
        ).data
