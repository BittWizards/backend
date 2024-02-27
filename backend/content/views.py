from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from content.models import Content
from content.serializers import (
    ContentSerializer,
    NewContentSerializer,
    PostContentSerializer,
)


class ContentViewSet(viewsets.ModelViewSet):
    queryset = (
        Content.objects.all()
        .prefetch_related("ambassador")
        .group("ambassador")
        .annotate(review_count=Sum("is_review"))
    )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostContentSerializer
        return ContentSerializer

    @action(methods=["get"], detail=False, url_path="new")
    def new_content(self, request, *args, **kwargs):
        queryset = Content.objects.filter(accepted=False)
        serializer = NewContentSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)
