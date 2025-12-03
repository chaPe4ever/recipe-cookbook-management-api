from rest_framework.serializers import ModelSerializer

from cookbook.serializers import CookbookSerializer, AuthorSerializer
from ingredient.models import Ingredient
from ingredient.serializers import IngredientSerializer
from recipe.models import Recipe


class RecipeSerializer(ModelSerializer):
    # Use nested serializer for creating ingredients
    ingredients = IngredientSerializer(many=True, required=False)
    cookbooks = CookbookSerializer(many=True, read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "difficulty",
            "author",
            "favorite",
            "cookbooks",
            "ingredients",
        ]
        read_only_fields = ["author", "cookbooks"]
        ref_name = "Recipe"

    def create(self, validated_data):
        # Extract ingredients data
        ingredients_data = validated_data.pop("ingredients", [])

        # Create the recipe
        recipe = Recipe.objects.create(**validated_data)

        # Create and associate ingredients
        for ingredient_data in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(
                title=ingredient_data["title"],
                defaults={"description": ingredient_data.get("description", "")},
            )
            recipe.ingredients.add(ingredient)

        return recipe

    def update(self, instance, validated_data):
        # Extract ingredients data
        ingredients_data = validated_data.pop("ingredients", None)

        # Update recipe fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update ingredients if provided
        if ingredients_data is not None:
            instance.ingredients.clear()
            for ingredient_data in ingredients_data:
                ingredient, created = Ingredient.objects.get_or_create(
                    title=ingredient_data["title"],
                    defaults={"description": ingredient_data.get("description", "")},
                )
                instance.ingredients.add(ingredient)

        return instance
