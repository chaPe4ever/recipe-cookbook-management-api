from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from author.models import Author

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]
        ref_name = "AuthorUser"


class AuthorSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Author
        fields = ["user"]
        ref_name = "Author"
