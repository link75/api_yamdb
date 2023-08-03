from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, generate_token, signup

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', generate_token, name='generate_token'),
]
