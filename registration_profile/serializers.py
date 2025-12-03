from django.contrib.auth import get_user, get_user_model
from rest_framework.serializers import ModelSerializer

from registration_profile.models import RegistrationProfile

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class RegistrationProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = RegistrationProfile
        fields = ["id", "user"]
