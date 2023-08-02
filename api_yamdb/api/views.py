from rest_framework.filters import SearchFilter
from rest_framework.permissions import SAFE_METHODS

from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializerGET, TitleSerializerPOST)
from .mixins import CreateDestroyListViewSet
from .permissions import IsAdminOrReadOnly

from reviews.models import Category, Genre, Title


class CategoryViewSet(CreateDestroyListViewSet):
    """Вьюсет для получения категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyListViewSet):
    """Вьюсет для получения жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(CreateDestroyListViewSet):
    """Вьюсет для получения произведений."""
    queryset = Title.objects.all()
    filter_backends = (SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in SAFE_METHODS:
            return TitleSerializerGET
        return TitleSerializerPOST
