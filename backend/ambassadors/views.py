from django.db.models import Count, OuterRef, Prefetch, Subquery
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.request import Request
from rest_framework.response import Response

from ambassadors.models import Ambassador, YandexProgramm
from ambassadors.serializers import (
    AmbassadorContentSerializer,
    AmbassadorListSerializer,
    AmbassadorPromocodeSerializer,
    AmbassadorSerializer,
    FormCreateAmbassadorSerializer,
    YandexProgrammSerializer,
)
from content.mixins import ListViewSet
from content.models import Content, Promocode
from openapi.ambassadors_schema import (
    ambassador_extend_schema_view,
    form_create_schema,
    yandex_programms_extend_schema_view,
)
from openapi.contents_schema import (
    all_promocodes_of_ambassador,
    allcontent_to_ambassador,
)


@extend_schema_view(**ambassador_extend_schema_view)
class AmbassadorViewSet(viewsets.ModelViewSet):
    """Viewset модели Ambassador."""

    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action == "list":
            return AmbassadorListSerializer
        return AmbassadorSerializer

    @extend_schema(**form_create_schema)
    @action(detail=False, url_path="form", methods=("post",))
    def form(self, request):
        """
        Создание экземпляра амбассадора через форму.
        """
        serializer = FormCreateAmbassadorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(**allcontent_to_ambassador)
    @action(detail=False, url_path=r"(?P<ambassador_id>\d+)/content")
    def contents(self, request: Request, ambassador_id: int) -> Response:
        """Весь контент амбассадора."""

        queryset = (
            Ambassador.objects.filter(id=ambassador_id)
            .prefetch_related(
                Prefetch(
                    "my_content",
                    queryset=Content.objects.filter(
                        accepted=True
                    ).prefetch_related("documents"),
                )
            )
            .annotate(
                rating=Subquery(
                    Content.objects.filter(
                        ambassador=OuterRef("pk"), accepted=True
                    )
                    .values("ambassador")
                    .annotate(count=Count("pk"))
                    .values("count")
                ),
            )[0]
        )
        serializer = AmbassadorContentSerializer(
            queryset, many=False, context={"request": request}
        )
        return Response(serializer.data)

    @extend_schema(**all_promocodes_of_ambassador)
    @action(detail=False, url_path=r"(?P<ambassador_id>\d+)/promocodes")
    def promocodes(self, request: Request, ambassador_id: int) -> Response:
        """Все промокоды амбассадора."""

        queryset = Ambassador.objects.filter(
            id=ambassador_id
        ).prefetch_related(
            Prefetch("my_promocode", queryset=Promocode.objects.all())
        )[
            0
        ]
        serializer = AmbassadorPromocodeSerializer(
            queryset, many=False, context={"request": request}
        )
        return Response(serializer.data)


@extend_schema_view(**yandex_programms_extend_schema_view)
class YandexProgrammViewSet(ListViewSet):
    """
    Viewset модели YandexProgramm.
    """

    queryset = YandexProgramm.objects.all()
    serializer_class = YandexProgrammSerializer


@extend_schema(exclude=True)
@api_view(["GET"])
def get_ambassador_by_tg_acc(request: Request, tg_acc: str) -> Response:
    """Возвращаем данные амбассадора по его username в telegram."""
    ambassador = get_object_or_404(Ambassador, tg_acc=tg_acc)
    serializer = AmbassadorSerializer(instance=ambassador)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
