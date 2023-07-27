from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GengreViewSet, ReviewViewSet

router = DefaultRouter()
router.register('genres', GengreViewSet)
router.register('reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
