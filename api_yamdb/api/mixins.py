from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class CreateDestroyListMixin(CreateModelMixin, DestroyModelMixin,
                             ListModelMixin, GenericViewSet):
    ...
