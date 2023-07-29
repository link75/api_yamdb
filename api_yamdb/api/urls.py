from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'reviews/(?P<review_id>\d+)/comments', CommentViewSet,
                basename='comments')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')

urlpatterns = [
    path('v1/', include(router.urls)),
]
