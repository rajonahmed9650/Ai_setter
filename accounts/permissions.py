from rest_framework.permissions import BasePermission


class IsOwnerAdmin(BasePermission):
    """
    Allow access only to Owner/Admin users.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff   # ✅ admin/owner check
        )
