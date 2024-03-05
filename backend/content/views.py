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
from django.db.models import Count, OuterRef, Subquery
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response


@extend_schema(tags=["Промокоды"])
class PromoCodeViewSet(ListCreateDestroyViewSet):
    queryset = Promocode.objects.all().prefetch_related("ambassador")

    def get_serializer_class(self):
        if self.request.method in ["POST"]:
            return PostPromocodeSerializer
        return PromocodeSerializer


@extend_schema(tags=["Контент"])
class AllContentsViewSet(ListViewSet):
    """Просмотр всего контента всех амбассадоров"""

    serializer_class = AllContentSerializer

    def get_queryset(self):
        queryset = Ambassador.objects.annotate(
            rating=Subquery(
                Content.objects.filter(
                    ambassador=OuterRef("pk"), accepted=True
                )
                .values("ambassador")
                .annotate(count=Count("pk"))
                .values("count")
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
        )
        return queryset

    @action(methods=["get"], detail=False, url_path="new")
    def new_content(self, request, *args, **kwargs):
        """Просмотр новых заявок на контент"""
        queryset = Content.objects.filter(accepted=False).select_related(
            "ambassador"
        )
        serializer = NewContentSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


@extend_schema(tags=["Контент"])
class ContentDetailViewSet(CreateRetrieveUpdateDeleteViewSet):
    """Просмотр, создание, изменение, удаление карточки контента"""

    queryset = Content.objects.all().select_related("ambassador")

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return PostContentSerializer
        return ContentSerializers
