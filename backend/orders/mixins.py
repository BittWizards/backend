from rest_framework import mixins, viewsets


class CreateRetrieveMixin(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pass
