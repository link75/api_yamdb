from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin)


class IsAdminOrReadOnly(IsAdmin):

    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                or request.method in SAFE_METHODS)


class IsAuthorAdminModerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (obj.author == request.user
                    or (request.user.is_authenticated
                        and (request.user.is_moderator
                             or request.user.is_admin))
                    )
                )
