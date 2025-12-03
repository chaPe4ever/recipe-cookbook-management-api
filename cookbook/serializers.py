from rest_framework.serializers import ModelSerializer

from cookbook.models import Cookbook


class CookbookSerializer(ModelSerializer):
    class Meta:
        model = Cookbook
        fields = ["id", "title", "description", "recipes"]
