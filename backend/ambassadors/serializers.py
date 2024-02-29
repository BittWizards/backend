from rest_framework import serializers

from .models import (
    Actions,
    Ambassador,
    AmbassadorActions,
    AmbassadorAddress,
    AmbassadorSize,
    MessageToAmbassador,
    SendingMessage,
    YandexProgramm,
)


class YandexProgrammSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели YandexProgramm
    """

    class Meta:
        model = YandexProgramm
        fields = ("title", "description")


class AmbassadorSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Ambassador.
    """

    class Meta:
        model = Ambassador
        fields = (
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "gender",
            "ya_programm",
            "phone",
            "tg_acc",
            "education",
            "work_now",
            "status",
            "created",
        )


class ActionsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Actions.
    """

    class Meta:
        model = Actions
        fields = ("title", "description")


class AmbassadorActionsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели AmbassadorActions.
    """

    class Meta:
        model = AmbassadorActions
        fields = ("ambassador_id", "action")


class AmbassadorAddressSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели AmbassadorAddress.
    """

    class Meta:
        model = AmbassadorAddress
        fields = (
            "county",
            "city",
            "street_home",
            "post_index",
            "ambassador_id",
        )


class AmbassadorSizeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели AmbassadorSize.
    """

    class Meta:
        model = AmbassadorSize
        fields = ("ambassador_id", "clothes_size", "foot_size")


class SendingMessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели SendingMessage.
    """

    class Meta:
        model = SendingMessage
        fields = ("title", "description", "created", "supervisor_id", "sent")


class MessageToAmbassadorSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели MessageToAmbassador.
    """

    class Meta:
        model = MessageToAmbassador
        fields = ("ambassador_id", "sending_message_id")
