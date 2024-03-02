from rest_framework import serializers

from .models import (
    Ambassador,
    AmbassadorActions,
    AmbassadorAddress,
    AmbassadorSize,
    YandexProgramm,
)


class YandexProgrammSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели YandexProgramm
    """

    class Meta:
        model = YandexProgramm
        fields = ("title", "description")


class AmbassadorAddressSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели YandexProgramm
    """

    class Meta:
        model = AmbassadorAddress
        fields = ("country", "city", "street_home", "post_index")


class AmbassadorActionsSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели AmbassadorActions
    """

    action = serializers.CharField(source="action.title")

    class Meta:
        model = AmbassadorActions
        fields = ("action",)


class AmbassadorSizeSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели AmbassadorSize
    """

    class Meta:
        model = AmbassadorSize
        fields = (
            "clothes_size",
            "foot_size",
        )


class AmbassadorListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для выдачи списка объектов модели Ambassador
    """

    ya_programm = YandexProgrammSerializer()

    class Meta:
        model = Ambassador
        fields = (
            "first_name",
            "last_name",
            "middle_name",
            "ya_programm",
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

    class Meta:
        model = Ambassador
        fields = (
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
