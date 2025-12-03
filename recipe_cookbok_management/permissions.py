from rest_framework.permissions import BasePermission
import logging

logger = logging.getLogger(__name__)


class IsInGroup(BasePermission):
    """
    Base class to check if user is in a specific group.
    """

    required_groups = []

    def has_permission(self, request, view):
        logger.info(f"Checking permission for user: {request.user}")
        logger.info(f"Is authenticated: {request.user.is_authenticated}")

        if not request.user.is_authenticated:
            logger.warning("User is not authenticated")
            return False

        user_groups = list(request.user.groups.values_list("name", flat=True))
        logger.info(f"User groups: {user_groups}")
        logger.info(f"Required groups: {self.required_groups}")

        # Check if user is in any of the required groups
        has_perm = request.user.groups.filter(name__in=self.required_groups).exists()
        logger.info(f"Has permission: {has_perm}")

        return has_perm


class IsAuthor(IsInGroup):
    """
    Only users in 'Authors' group can access.
    """

    required_groups = ["Authors"]


class IsModerator(IsInGroup):
    """
    Only users in 'Moderators' group can access.
    """

    required_groups = ["Moderators"]


class IsAdminOrModerator(IsInGroup):
    """
    Users in 'Admins' or 'Moderators' groups can access.
    """

    required_groups = ["Admins", "Moderators"]


class IsAuthorOrReadOnly(BasePermission):
    """
    Authors can create/edit, everyone else can only read.
    """

    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS for everyone
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Write permissions only for authenticated authors
        if not request.user.is_authenticated:
            logger.warning("User is not authenticated for write operation")
            return False

        is_author = request.user.groups.filter(name="Authors").exists()
        logger.info(f"User {request.user.username} is author: {is_author}")
        logger.info(
            f"User groups: {list(request.user.groups.values_list('name', flat=True))}"
        )

        return is_author


class IsOwnerOrModerator(BasePermission):
    """
    Only the owner of the object or a moderator can edit/delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions for everyone
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        if not request.user.is_authenticated:
            return False

        # Moderators can do anything
        if request.user.groups.filter(name__in=["Moderators", "Admins"]).exists():
            return True

        # Check if user owns the object
        if hasattr(obj, "author") and obj.author is not None:
            return obj.author.user == request.user

        return False
