from django.contrib import admin

from ingredient.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass
