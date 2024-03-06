from rest_framework import mixins, viewsets


class RetrieveMixin(
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pass
