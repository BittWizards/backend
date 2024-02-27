from rest_framework import serializers

from content.models import Content


class ContentSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра всех пользователей с их контентом"""

    class Meta:
        model = Content
        fields = [
            "ambassador",
        ]


class PostContentSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заявки на контент"""

    pass


class NewContentSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения заявок на контент"""

    pass
