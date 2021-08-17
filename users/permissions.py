from rest_framework import permissions

class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        print('obj is ',obj)
        print('request email is ',request.user.email)
        return obj == request.user

        