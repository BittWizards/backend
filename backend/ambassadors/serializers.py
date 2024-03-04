from content.serializers import (
    ContentsForAmbassadorSerializer,
    PromocodeForAmbassadorSerializer,
)
from rest_framework import serializers

from .models import (
    Actions,
    Ambassador,
    AmbassadorActions,
    AmbassadorAddress,
    AmbassadorSize,
    YandexProgramm,
)


class YandexProgrammSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели YandexProgramm.
    """

    class Meta:
        model = YandexProgramm
        fields = ("title", "description")


class AmbassadorAddressSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели AmbassadorAddress.
    """

    class Meta:
        model = AmbassadorAddress
        fields = ("country", "city", "street_home", "post_index")


class AmbassadorActionsSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели AmbassadorActions
    """

    title = serializers.CharField(source="action.title")
    # description = serializers.CharField(source="action.description")

    class Meta:
        model = AmbassadorActions
        fields = ("title",)


class AmbassadorSizeSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели AmbassadorSize.
    """

    class Meta:
        model = AmbassadorSize
        fields = (
            "clothes_size",
            "foot_size",
        )


class AmbassadorListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для выдачи списка объектов модели Ambassador.
    """

    ya_programm = YandexProgrammSerializer()

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "image",
            "first_name",
            "last_name",
            "middle_name",
            "ya_programm",
            "tg_acc",
            "status",
            "created",
        )


class AmbassadorSerializer(serializers.ModelSerializer):
    """
    Сериализатор единственного объекта модели Ambassador.
    """

    ya_programm = YandexProgrammSerializer()
    address = AmbassadorAddressSerializer()
    size = AmbassadorSizeSerializer()
    actions = AmbassadorActionsSerializer(many=True)
    created = serializers.ReadOnlyField()

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "image",
            "first_name",
            "last_name",
            "middle_name",
            "gender",
            "phone",
            "email",
            "tg_acc",
            "ya_programm",
            "education",
            "work",
            "address",
            "size",
            "actions",
            "status",
            "created",
        )

    def create(self, validated_data):
        ya_programm = validated_data.pop("ya_programm")
        address = validated_data.pop("address")
        size = validated_data.pop("size")
        actions_data = validated_data.pop("actions")
        ambassador = Ambassador.objects.create(
            ya_programm=YandexProgramm.objects.get_or_create(**ya_programm)[0],
            **validated_data,
        )
        address_data = AmbassadorAddress.objects.create(
            **address,
            ambassador_id=ambassador,
        )
        size_data = AmbassadorSize.objects.create(
            ambassador_id=ambassador,
            **size,
        )
        for action_data in actions_data:
            current_action = Actions.objects.get_or_create(
                **action_data["action"],
            )
            AmbassadorActions.objects.create(
                action=current_action[0],
                ambassador_id=ambassador,
            )

        ambassador.address = address_data
        ambassador.size = size_data
        ambassador.save()
        return ambassador

    def update(self, instance, validated_data):
        if "ya_programm" in validated_data:
            ya_programm = validated_data.pop("ya_programm")
            instance.ya_programm = YandexProgramm.objects.get_or_create(
                **ya_programm
            )[0]
        if "address" in validated_data:
            address = validated_data.pop("address")
            AmbassadorAddress.objects.get_or_create(
                **address, ambassador_id=instance
            )
        if "size" in validated_data:
            size = validated_data.pop("size")
            AmbassadorSize.objects.get_or_create(
                ambassador_id=instance,
                **size,
            )
        if "actions" in validated_data:
            actions_data = validated_data.pop("actions")
            for action_data in actions_data:
                current_action = Actions.objects.get_or_create(
                    **action_data["action"]
                )
                AmbassadorActions.objects.create(
                    action=current_action[0], ambassador_id=instance
                )

        instance.save()
        return instance


class AmbassadorContentPromoSerializer(serializers.ModelSerializer):
    """Родительский сериализатор для контента промокодов."""

    city = serializers.SerializerMethodField()

    class Meta:
        model = Ambassador
        fields = [
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
        ]

    def get_city(self, obj) -> str:
        city = AmbassadorAddress.objects.get(ambassador_id=obj.id).city
        return city


class AmbassadorContentSerializer(AmbassadorContentPromoSerializer):
    """Сериализатор для контента конкретного амбассадора."""

    my_content = ContentsForAmbassadorSerializer(many=True)

    class Meta(AmbassadorContentPromoSerializer.Meta):
        fields = AmbassadorContentPromoSerializer.Meta.fields + ["my_content"]


class AmbassadorPromocodeSerializer(AmbassadorContentPromoSerializer):
    """Сериализатор для промокодов конкретного амбассадора."""

    my_promocode = PromocodeForAmbassadorSerializer(many=True)

    class Meta(AmbassadorContentPromoSerializer.Meta):
        fields = AmbassadorContentPromoSerializer.Meta.fields + [
            "my_promocode"
        ]
