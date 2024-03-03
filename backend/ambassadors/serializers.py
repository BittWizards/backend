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
    description = serializers.CharField(source="action.description")

    class Meta:
        model = AmbassadorActions
        fields = ("title", "description")


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
            "first_name",
            "last_name",
            "middle_name",
            "gender",
            "phone",
            "email",
            "tg_acc",
            "ya_programm",
            "education",
            "work_now",
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
            **address, ambassador_id=ambassador
        )
        size_data = AmbassadorSize.objects.create(
            ambassador_id=ambassador,
            **size,
        )
        for action_data in actions_data:
            current_action = Actions.objects.get_or_create(
                **action_data["action"]
            )
            AmbassadorActions.objects.create(
                action=current_action[0], ambassador_id=ambassador
            )

        ambassador.address = address_data
        ambassador.size = size_data
        ambassador.save()
        return ambassador

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get(
            "last_name", instance.last_name
        )
        instance.middle_name = validated_data.get(
            "middle_name", instance.middle_name
        )
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.tg_acc = validated_data.get("tg_acc", instance.tg_acc)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.education = validated_data.get(
            "education", instance.education
        )
        instance.work_now = validated_data.get("work_now", instance.work_now)
        instance.status = validated_data.get("status", instance.status)

        ya_programm = validated_data.pop("ya_programm")
        address = validated_data.pop("address")
        size = validated_data.pop("size")
        actions_data = validated_data.pop("actions")

        address_data = AmbassadorAddress.objects.get_or_create(
            **address, ambassador_id=instance
        )
        size_data = AmbassadorSize.objects.get_or_create(
            ambassador_id=instance,
            **size,
        )
        for action_data in actions_data:
            current_action = Actions.objects.get_or_create(
                **action_data["action"]
            )
            AmbassadorActions.objects.create(
                action=current_action[0], ambassador_id=instance
            )

        instance.ya_programm = YandexProgramm.objects.get_or_create(
            **ya_programm
        )[0]

        instance.save()

        return instance
