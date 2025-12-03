from django.urls import path

from recipe.views import ListCreateRecipeView, RetrieveUpdateDestroyRecipeView

urlpatterns = [
    path("", ListCreateRecipeView.as_view()),
    path("<int:pk>/", RetrieveUpdateDestroyRecipeView.as_view()),
]
