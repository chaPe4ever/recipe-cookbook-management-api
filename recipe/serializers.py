from rest_framework.serializers import ModelSerializer

from recipe.models import Recipe


class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "difficulty",
            "authors",
            "favorite",
            "cookbooks",
            "ingredients",
        ]
