from rest_framework import serializers

from ambassadors.models import (
    Actions,
    Ambassador,
    AmbassadorActions,
    AmbassadorAddress,
    AmbassadorSize,
    YandexProgramm,
)
from ambassadors.validators import (
    gender_validator,
    telegram_validator,
    tg_acc_validator,
)
from content.models import Content, Promocode


class YandexProgrammSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели YandexProgramm.
    """

    class Meta:
        model = YandexProgramm
        fields = ("title",)


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

    ya_programm = serializers.CharField(source="ya_programm.title")

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
            "achievement",
            "created",
        )


class AmbassadorSerializer(serializers.ModelSerializer):
    """
    Сериализатор единственного объекта модели Ambassador.
    """

    ya_programm = serializers.CharField(source="ya_programm.title")
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
            "tg_id",
            "ya_programm",
            "purpose",
            "education",
            "work",
            "address",
            "size",
            "actions",
            "status",
            "achievement",
            "created",
        )

    def validate(self, data):
        try:
            tg_acc = data.get("tg_acc")
        except KeyError as error:
            return error

        data["tg_id"] = telegram_validator(tg_acc)
        return data

    def create(self, validated_data):
        ya_programm = validated_data.pop("ya_programm")
        address = validated_data.pop("address")
        size = validated_data.pop("size")
        actions_data = validated_data.pop("actions")
        ambassador = Ambassador.objects.create(
            ya_programm=YandexProgramm.objects.get_or_create(
                title=ya_programm["title"]
            )[0],
            **validated_data,
        )
        # TODO Валидация
        address_data = AmbassadorAddress.objects.create(
            **address,
            ambassador_id=ambassador,
        )
        # TODO Валидация
        size_data = AmbassadorSize.objects.create(
            ambassador_id=ambassador,
            **size,
        )
        for action_data in actions_data:
            # TODO Валидация
            current_action = Actions.objects.get_or_create(
                **action_data["action"],
            )
            # TODO Валидация
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
            # TODO Валидация
            instance.ya_programm = YandexProgramm.objects.get_or_create(
                **ya_programm
            )[0]
        if "address" in validated_data:
            address = validated_data.pop("address")
            # TODO Валидация
            AmbassadorAddress.objects.get_or_create(
                **address, ambassador_id=instance
            )
        if "size" in validated_data:
            size = validated_data.pop("size")
            # TODO Валидация
            AmbassadorSize.objects.get_or_create(
                ambassador_id=instance,
                **size,
            )
        if "actions" in validated_data:
            actions_data = validated_data.pop("actions")
            for action_data in actions_data:
                # TODO Валидация
                current_action = Actions.objects.get_or_create(
                    **action_data["action"]
                )
                # TODO Валидация
                AmbassadorActions.objects.create(
                    action=current_action[0], ambassador_id=instance
                )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def validate(self, data):
        if "tg_acc" in data:
            tg_acc_validator(data)
        return data


class ShortAmbassadorSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения короткого списка полей амбассадора
    Поля: id, image, first_name, last_name, status, tg_acc, ya_programm"""

    ya_programm = serializers.CharField(source="ya_programm.title")

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "image",
            "first_name",
            "last_name",
            "status",
            "achievement",
            "tg_acc",
            "ya_programm",
        )


class FormCreateAmbassadorSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания амбассадора через YandexForm.
    """

    full_name = serializers.CharField()
    gender = serializers.CharField()
    ya_programm = serializers.CharField()
    purpose = serializers.CharField(required=False)
    purpose_extra = serializers.CharField(required=False)
    foot_size = serializers.IntegerField()
    clothes_size = serializers.CharField()
    country = serializers.CharField()
    city = serializers.CharField()
    street_home = serializers.CharField()
    post_index = serializers.IntegerField()
    actions = serializers.CharField()

    class Meta:
        model = Ambassador
        fields = (
            "full_name",
            "gender",
            "ya_programm",
            "country",
            "city",
            "street_home",
            "post_index",
            "email",
            "phone",
            "tg_acc",
            "education",
            "work",
            "purpose",
            "purpose_extra",
            "actions",
            "clothes_size",
            "foot_size",
            "extra_info",
        )

    def validate(self, data):
        try:
            gender = data.get("gender")
            tg_acc = data.get("tg_acc")
        except KeyError as error:
            return error

        data["tg_id"] = telegram_validator(tg_acc)
        data["gender"] = gender_validator(gender)
        return data

    def create(self, validated_data):
        full_name = validated_data.pop("full_name")
        ya_programm = validated_data.pop("ya_programm")
        actions = validated_data.pop("actions")
        purpose = validated_data.get("purpose")
        foot_size = validated_data.pop("foot_size")
        clothes_size = validated_data.pop("clothes_size")
        country = validated_data.pop("country")
        city = validated_data.pop("city")
        street_home = validated_data.pop("street_home")
        post_index = validated_data.pop("post_index")

        if not purpose:
            purpose = validated_data.pop("purpose_extra")
        else:
            purpose = validated_data.pop("purpose")

        prepared_fio = full_name.split()

        ambassador = Ambassador.objects.create(
            ya_programm=YandexProgramm.objects.get_or_create(
                title=ya_programm
            )[0],
            purpose=purpose,
            last_name=prepared_fio[0],
            first_name=prepared_fio[1],
            middle_name=prepared_fio[2],
            **validated_data,
        )
        address_data = AmbassadorAddress.objects.create(
            ambassador_id=ambassador,
            country=country,
            city=city,
            street_home=street_home,
            post_index=post_index,
        )
        size_data = AmbassadorSize.objects.create(
            ambassador_id=ambassador,
            clothes_size=clothes_size,
            foot_size=foot_size,
        )
        action_data = actions.split(", ")
        for action in action_data:
            current_action = Actions.objects.get_or_create(
                title=action,
            )
            AmbassadorActions.objects.create(
                action=current_action[0],
                ambassador_id=ambassador,
            )

        ambassador.address = address_data
        ambassador.size = size_data
        ambassador.save()
        return ambassador

    def to_representation(self, instance):
        return AmbassadorSerializer(instance).data


class AmbassadorContentPromoSerializer(serializers.ModelSerializer):
    """Родительский сериализатор для контента промокодов."""

    city = serializers.SerializerMethodField()
    ya_programm = serializers.CharField(source="ya_programm.title")

    class Meta:
        model = Ambassador
        fields = [
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
        ]

    def get_city(self, obj) -> str:
        city = AmbassadorAddress.objects.get(ambassador_id=obj.id).city
        return city


class ContentsForAmbassadorSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения контента конкретного амбассадора."""

    documents = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ("id", "created_at", "platform", "link", "documents")

    def get_documents(self, obj) -> int:
        return obj.documents.count()


class PromocodeForAmbassadorSerializer(serializers.ModelSerializer):
    """Сериализатор для промокодов."""

    class Meta:
        model = Promocode
        fields = ("id", "promocode", "is_active", "created_at")


class AmbassadorContentSerializer(AmbassadorContentPromoSerializer):
    """Сериализатор для контента конкретного амбассадора."""

    my_content = ContentsForAmbassadorSerializer(many=True)
    rating = serializers.IntegerField(default=0)

    class Meta(AmbassadorContentPromoSerializer.Meta):
        fields = AmbassadorContentPromoSerializer.Meta.fields + [
            "my_content",
            "rating",
        ]


class AmbassadorPromocodeSerializer(AmbassadorContentPromoSerializer):
    """Сериализатор для промокодов конкретного амбассадора."""

    my_promocode = PromocodeForAmbassadorSerializer(many=True)

    class Meta(AmbassadorContentPromoSerializer.Meta):
        fields = AmbassadorContentPromoSerializer.Meta.fields + [
            "my_promocode"
        ]


class AmbassadorInMessageSerializer(serializers.ModelSerializer):
    tg_acc = serializers.CharField(required=False, read_only=True)
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Ambassador
        fields = ("id", "tg_acc")
