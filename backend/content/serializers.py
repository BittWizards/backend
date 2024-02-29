from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from ambassadors.models import Ambassador, AmbassadorAddress
from content.models import Content, Documents, Promocode


class AmbassadorForNewContentSerializer(serializers.ModelSerializer):
    """Сериализатор для амбассадора в новой заявке на контент"""

    class Meta:
        model = Ambassador
        fields = ("last_name", "first_name", "tg_acc", "status")


class NewContentSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения заявок на контент"""

    ambassador = AmbassadorForNewContentSerializer(read_only=True)

    class Meta:
        model = Content
        fields = (
            "id",
            "ambassador",
            "created_at",
        )


class AllContentSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра всех пользователей с их контентом"""

    review_count = serializers.IntegerField(default=0)
    habr_count = serializers.IntegerField(default=0)
    rating = serializers.IntegerField(default=0)
    vc_count = serializers.IntegerField(default=0)
    youtube_count = serializers.IntegerField(default=0)
    tg_count = serializers.IntegerField(default=0)
    instagram_count = serializers.IntegerField(default=0)
    linledin_count = serializers.IntegerField(default=0)
    other_count = serializers.IntegerField(default=0)

    class Meta:
        model = Ambassador
        fields = (
            "id",
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
            "linledin_count",
            "other_count",
        )


class ContentsForAmbassadorSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения контента конкретного амбассадора"""

    documents = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ("id", "created_at", "platform", "link", "documents")

    def get_documents(self, obj) -> int:
        return obj.documents.count()


class AmbassadorContentSerializer(serializers.ModelSerializer):
    """Сериализатор для контента конкретного амбассадора"""

    my_content = ContentsForAmbassadorSerializer(many=True)
    city = serializers.SerializerMethodField()

    class Meta:
        model = Ambassador
        fields = (
            "last_name",
            "first_name",
            "middle_name",
            "status",
            "tg_acc",
            "email",
            "phone",
            "city",
            "my_content",
        )

    def get_city(self, obj) -> str:
        city = AmbassadorAddress.objects.get(ambassador_id=obj.id).city
        return city


class AmbassadorForContentSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения данных амбассадора в карточке контента"""

    city = serializers.SerializerMethodField()
    email = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Ambassador
        fields = (
            "last_name",
            "first_name",
            "middle_name",
            "status",
            "tg_acc",
            "email",
            "phone",
            "city",
        )

    def get_city(self, obj) -> str:
        city = AmbassadorAddress.objects.get(ambassador_id=obj.id).city
        return city


class ContentSerializers(serializers.ModelSerializer):
    """Сериализатор для карточек контента"""

    ambassador = AmbassadorForContentSerializer()
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
    """Сериализатор для POST, PATCH запросов карточек контента"""

    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    tg_acc = serializers.CharField()
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
        fio = validated_data.pop("name")
        tg_acc = validated_data.pop("tg_acc")
        documents = validated_data.pop("files").split(",")
        ambassador = get_object_or_404(Ambassador, tg_acc=tg_acc)
        with transaction.atomic():
            content = Content.objects.create(
                **validated_data, ambassador=ambassador
            )
            docs_to_create = [
                Documents(content=content, document=docs) for docs in documents
            ]
            Documents.objects.bulk_create(docs_to_create)

        return content

    def to_representation(self, instance):
        return ContentSerializers(
            instance, context={"request": self.context.get("request")}
        ).data


class PromocodeSerializer(serializers.ModelSerializer):
    """Сериализатор для промокодов"""

    ambassador = AmbassadorForNewContentSerializer(read_only=True)

    class Meta:
        model = Promocode
        fields = ("id", "promocode", "is_active", "created_at", "ambassador")


class PostPromocodeSerializer(serializers.ModelSerializer):
    """Сериализатор для промокодов"""

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

    def to_representation(self, instance):
        return PromocodeSerializer(
            instance, context={"request": self.context.get("request")}
        ).data
