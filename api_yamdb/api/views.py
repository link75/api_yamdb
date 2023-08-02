from rest_framework import permissions, viewsets, filters
from rest_framework.permissions import SAFE_METHODS
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404


from .serializers import (ReviewSerializer, CommentSerializer, GenreSerializer, TitleSerializerGET, TitleSerializerPOST)
from reviews.models import Review, Title, Genre, Category
from .permission import IsAdminModeratorOwnerOrReadOnly, IsAdminOrReadOnly
from .mixins import CreateDestroyListViewSet


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
      
      
 class CategoryViewSet(CreateDestroyListViewSet):
    """Вьюсет для получения категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
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
