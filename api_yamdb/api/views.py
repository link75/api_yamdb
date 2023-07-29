from rest_framework import permissions, viewsets
from django.shortcuts import get_object_or_404

from .serializers import ReviewSerializer, CommentSerializer
from reviews.models import Review, Title
from .permission import IsAdminOrAuthorOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly)

    def get_permissions(self):
        if self.request.method not in ('GET'):
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticatedOrReadOnly(),)

    def get_queryset(self):
        review_title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return review_title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=review_title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly)

    def get_permissions(self):
        if self.request.method not in ('GET'):
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticatedOrReadOnly(),)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
