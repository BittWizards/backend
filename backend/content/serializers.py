import re

from ambassadors_project.constants import (
    ERROR_MESSAGE_PROMOCODE,
    PATTERN_PROMO,
)
from content.models import Content, Documents, Promocode
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ambassadors.models import Ambassador, AmbassadorAddress
from ambassadors.validators import tg_acc_validator


class ShortAmbassadorSerializer(serializers.ModelSerializer):
    """Сериализатор для амбассадора в новой заявке на контент."""

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "image",
            "last_name",
            "first_name",
            "ya_programm",
            "tg_acc",
            "status",
        )


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

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "image",
            "last_name",
            "first_name",
            "tg_acc",
            "rating",
            "review_count",
            "habr_count",
            "vc_count",
            "youtube_count",
            "tg_count",
            "instagram_count",
            "linkedin_count",
            "other_count",
        )


class ContentsForAmbassadorSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения контента конкретного амбассадора."""

    documents = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ("id", "created_at", "platform", "link", "documents")

    def get_documents(self, obj) -> int:
        return obj.documents.count()


class AmbassadorForContentPromoCardSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения данных амбассадора
     в карточках контента и промокодов.
    """

    city = serializers.SerializerMethodField()
    email = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "image",
            "last_name",
            "first_name",
            "middle_name",
            "status",
            "tg_acc",
            "email",
            "phone",
            "ya_programm",
            "city",
        )

    def get_city(self, obj) -> str:
        city = AmbassadorAddress.objects.get(ambassador_id=obj.id).city
        return city


class ContentSerializers(serializers.ModelSerializer):
    """Сериализатор для карточек контента."""

    ambassador = AmbassadorForContentPromoCardSerializer()
    id = serializers.IntegerField(required=False)

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
        )


class PostContentSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и изменения контента."""

    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    tg_acc = serializers.CharField(validators=(tg_acc_validator,))
    files = serializers.CharField(required=False)

    class Meta:
        model = Content
        fields = (
            "id",
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

    def create(self, validated_data) -> Content:
        fio = validated_data.pop("name")  # noqa: F841
        tg_acc = validated_data.pop("tg_acc")
        documents = None
        if "files" in validated_data:
            documents = validated_data.pop("files").split(",")
        ambassador = get_object_or_404(Ambassador, tg_acc=tg_acc)
        with transaction.atomic():
            content = Content.objects.create(
                **validated_data, ambassador=ambassador
            )
            if documents:
                docs_to_create = [
                    Documents(content=content, document=docs)
                    for docs in documents
                ]
                Documents.objects.bulk_create(docs_to_create)

        return content

    def update(self, instance, validated_data):
        super().update()
        if not validated_data.get("accepted"):
            return instance

    # функция подсчета контента и присвоения достижений

    def to_representation(self, instance):
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

    def deactivate(self, last_promo) -> None:
        for promocode in last_promo:
            promocode.is_active = False
            promocode.save()

    def create(self, validated_data):
        last_promo = Promocode.objects.filter(
            ambassador=validated_data["ambassador"], is_active=True
        )
        if last_promo:
            self.deactivate(last_promo)

        new_promo = Promocode.objects.create(**validated_data)
        return new_promo

    def validate(self, data):
        promocode = data.get("promocode")
        if not re.fullmatch(PATTERN_PROMO, promocode):
            raise ValidationError(ERROR_MESSAGE_PROMOCODE)
        return data

    def to_representation(self, instance):
        return PromocodeSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class PromocodeForAmbassadorSerializer(serializers.ModelSerializer):
    """Сериализатор для промокодов."""

    class Meta:
        model = Promocode
        fields = ("id", "promocode", "is_active", "created_at")
