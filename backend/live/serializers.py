from rest_framework import serializers

from .models import Push


class PushSerializer(serializers.ModelSerializer):
    class Meta:
        model = Push
        fields = ("name", "email")
