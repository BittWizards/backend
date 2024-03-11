from datetime import datetime

from django.db.models import Count, OuterRef, Subquery, Value, QuerySet
from django.db.models.functions import Coalesce
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from ambassadors.models import Ambassador
from content.mixins import (
    CreateRetrieveUpdateDeleteViewSet,
    ListCreateDestroyViewSet,
    ListViewSet,
)
from content.models import Content, ContentType, Platform, Promocode
from content.serializers import (
    AllContentSerializer,
    ContentSerializers,
    NewContentSerializer,
    PostContentSerializer,
    PostPromocodeSerializer,
    PromocodeSerializer,
)
from openapi.contents_schema import (
    allcontent_extended_schema_view,
    content_extended_schema_view,
    new_content_scheme,
    promocode_extend_schema_view,
)


@extend_schema_view(**promocode_extend_schema_view)
class PromoCodeViewSet(ListCreateDestroyViewSet):
    queryset = (
        Promocode.objects.all()
        .prefetch_related("ambassador")
        .order_by("-created_at")
    )

    def get_serializer_class(self) -> Serializer:
        if self.request.method in ["POST"]:
            return PostPromocodeSerializer
        return PromocodeSerializer


@extend_schema_view(**allcontent_extended_schema_view)
class AllContentsViewSet(ListViewSet):
    """Просмотр всего контента всех амбассадоров"""

    serializer_class = AllContentSerializer

    def get_queryset(self) -> QuerySet:
        queryset = Ambassador.objects.annotate(
            rating=Coalesce(
                Subquery(
                    Content.objects.filter(
                        ambassador=OuterRef("pk"), accepted=True
                    )
                    .values("ambassador")
                    .annotate(count=Count("pk"))
                    .values("count")
                ),
                Value(0),
            ),
            review_count=Subquery(
                Content.objects.filter(
                    ambassador=OuterRef("pk"),
                    accepted=True,
                    type=ContentType.REVIEW,
                )
                .values("ambassador")
                .annotate(count=Count("pk"))
                .values("count")
            ),
            habr_count=Subquery(
                Content.objects.filter(
                    ambassador=OuterRef("pk"),
                    accepted=True,
                    platform=Platform.HABR,
                )
                .values("ambassador")
                .annotate(count=Count("pk"))
                .values("count")
            ),
            vc_count=Subquery(
                Content.objects.filter(
                    ambassador=OuterRef("pk"),
                    accepted=True,
                    platform=Platform.VC,
                )
                .values("ambassador")
                .annotate(count=Count("pk"))
                .values("count")
            ),
            youtube_count=Subquery(
                Content.objects.filter(
                    ambassador=OuterRef("pk"),
                    accepted=True,
                    platform=Platform.YOUTUBE,
                )
                .values("ambassador")
                .annotate(count=Count("pk"))
                .values("count")
            ),
            tg_count=Subquery(
                Content.objects.filter(
                    ambassador=OuterRef("pk"),
                    accepted=True,
                    platform=Platform.TG,
                )
                .values("ambassador")
                .annotate(count=Count("pk"))
                .values("count")
            ),
            instagram_count=Subquery(
                Content.objects.filter(
                    ambassador=OuterRef("pk"),
                    accepted=True,
                    platform=Platform.INSTAGRAM,
                )
                .values("ambassador")
                .annotate(count=Count("pk"))
                .values("count")
            ),
            linkedin_count=Subquery(
                Content.objects.filter(
                    ambassador=OuterRef("pk"),
                    accepted=True,
                    platform=Platform.LINKEDIN,
                )
                .values("ambassador")
                .annotate(count=Count("pk"))
                .values("count")
            ),
            other_count=Subquery(
                Content.objects.filter(
                    ambassador=OuterRef("pk"),
                    accepted=True,
                    platform=Platform.OTHER,
                )
                .values("ambassador")
                .annotate(count=Count("pk"))
                .values("count")
            ),
            last_date=Coalesce(
                Subquery(
                    Content.objects.filter(
                        ambassador=OuterRef("pk"),
                        accepted=True,
                    )
                    .order_by("-created_at")
                    .values("ambassador")
                    .values("created_at")[:1]
                ),
                Value(datetime(2000, 1, 1, 0, 0, 0)),
            ),
        ).order_by("-rating", "-last_date")
        return queryset


@extend_schema_view(**content_extended_schema_view)
class ContentDetailViewSet(CreateRetrieveUpdateDeleteViewSet):
    """Просмотр, создание, изменение, удаление карточки контента"""

    queryset = (
        Content.objects.all()
        .select_related("ambassador")
        .prefetch_related("documents")
    )
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self) -> Serializer:
        if self.request.method in ["POST", "PATCH"]:
            return PostContentSerializer
        return ContentSerializers

    @extend_schema(**new_content_scheme)
    @action(methods=["get"], detail=False, url_path="new")
    def new_content(self, request, *args, **kwargs) -> Response:
        """Просмотр новых заявок на контент"""
        queryset = Content.objects.filter(accepted=False).select_related(
            "ambassador"
        )
        serializer = NewContentSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)
