from django.urls import path

from ingredient.views import (
    ListCreateIngredientsView,
    RetrieveUpdateDestroyIngredientView,
)

urlpatterns = [
    path("", ListCreateIngredientsView.as_view()),
    path("<int:pk>/", RetrieveUpdateDestroyIngredientView.as_view()),
]
