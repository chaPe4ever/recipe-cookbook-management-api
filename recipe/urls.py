from django.urls import path

from recipe.views import ListCreateRecipeView, RetrieveUpdateDestroyRecipeView

urlpatterns = [
    path("recipes/", ListCreateRecipeView.as_view()),
    path(
        "recipes/<int:pk>/",
        RetrieveUpdateDestroyRecipeView.as_view(),
    ),
]
