from rest_framework import permissions, viewsets, filters
from rest_framework.permissions import SAFE_METHODS
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend


from .serializers import (ReviewSerializer, CommentSerializer, GenreSerializer, TitleSerializer, TitlePOSTSerializer, CategorySerializer)
from reviews.models import Review, Title, Genre, Category
from .permissions import IsAdminModeratorOwnerOrReadOnly, IsAdminOrReadOnly
from .mixins import CreateDestroyListViewSet
from .filters import TitleFilter


class GenreViewSet(CreateDestroyListViewSet):
    """Вьюсет для получения жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения произведений."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by(
        'name'
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitlePOSTSerializer
        return TitleSerializer


class CategoryViewSet(CreateDestroyListViewSet):
    """Вьюсет для получения категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly)

    def get_queryset(self):
        review_title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return review_title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=review_title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
