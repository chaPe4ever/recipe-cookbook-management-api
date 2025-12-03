from django.urls import path

from ingredient.views import (
    ListCreateIngredientsView,
    RetrieveUpdateDestroyIngredientView,
)

urlpatterns = [
    path("ingredients/", ListCreateIngredientsView.as_view()),
    path("ingredients/<int:pk>/", RetrieveUpdateDestroyIngredientView.as_view()),
]
