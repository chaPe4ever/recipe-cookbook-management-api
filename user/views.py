from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from recipe_cookbok_management.permissions import IsOwnerOrModerator
from user.models import User
from user.serializers import UserSerializer, UserCreateSerializer


class ListCreateUserView(ListCreateAPIView):
    """
    GET: List all users (authenticated users only)
    POST: Create new user (public access for registration)
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        """Use different serializers for read vs write"""
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        """Allow public registration but require auth for listing"""
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]


class RetrieveUpdateDestroyUserView(RetrieveUpdateDestroyAPIView):
    """
    GET: View user profile
    PUT/PATCH: Update user profile (own profile only)
    DELETE: Delete user (own profile only)
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrModerator]
