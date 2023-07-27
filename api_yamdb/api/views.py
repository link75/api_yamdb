from rest_framework import filters, permissions, status, viewsets
from django.shortcuts import get_object_or_404

from .serializers import GenreSerializer, ReviewSerializer
from reviews.models import Genre, Review, Title


class GengreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = (permissions.IsAdminUser,)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Title, id=title_id)
        return review.reviews.all()
