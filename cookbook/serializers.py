from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from author.models import Author
from cookbook.models import Cookbook
from recipe.models import Recipe
from user.models import User


class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["id", "title"]
        ref_name = "CookbookRecipe"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]
        ref_name = "CookbookUser"


class AuthorSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Author
        fields = ["id", "user"]
        ref_name = "CookbookAuthor"


class CookbookSerializer(ModelSerializer):
    # For reading: show full recipe details
    recipes = RecipeSerializer(many=True, read_only=True)
    # For writing: accept recipe IDs
    recipe_ids = PrimaryKeyRelatedField(
        many=True,
        queryset=Recipe.objects.all(),
        write_only=True,
        required=False,
        source="recipes",
    )
    author = AuthorSerializer(read_only=True)
    recipe_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cookbook
        fields = [
            "id",
            "title",
            "description",
            "recipes",
            "recipe_ids",
            "recipe_count",
            "author",
        ]
        read_only_fields = ["author"]
