from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedAndOwnerOrReadOnlyOrStaff(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            (request.method in SAFE_METHODS) or (
                    request.user and request.user.is_authenticated and (obj.owner == request.user) or
                    request.user.is_staff)
        )

    def has_permission(self, request, view):
        return bool(
            (request.method in SAFE_METHODS) or (
                    request.user and request.user.is_authenticated or
                    request.user.is_staff)
        )


class IsAuthenticatedAndOwnerOrReadOnlyOrStaffForTags(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            (request.user and
             request.user.is_staff
             )
        )
