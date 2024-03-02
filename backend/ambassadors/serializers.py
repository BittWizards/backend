from rest_framework import serializers

from ambassadors.models import Ambassador


class AmbassadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambassador
        exclude = ("tg_id",)
