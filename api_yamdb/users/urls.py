from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, confirmation_code, registration

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
    path("auth/signup/", registration),
    path("auth/token/", confirmation_code),
]
