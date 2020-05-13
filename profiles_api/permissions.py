from rest_framework import permissions # provides a base permissions class


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """
        Check user is trying to edit their own profile
        Every time the request is made, DRF will call this function
        and it will pass in the request object, the view, and
        the actual object we are checking permissions against.
        """
        if request.method in permissions.SAFE_METHODS: # HTTP get method (methods that don't require any changes to the object)
            return True

        return obj.id == request.user.id # checks if the object they are updating matches their authenticated user profile that is
                                         # added to the authentication of the request


class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id
