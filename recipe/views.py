from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from author.models import Author
from recipe.models import Recipe
from recipe_cookbok_management.permissions import IsAuthorOrReadOnly, IsOwnerOrModerator
from recipe.serializers import RecipeSerializer


class ListCreateRecipeView(ListCreateAPIView):
    """
    GET: Anyone can view recipes
    POST: Only users in 'Authors' group can create
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # Get the Author instance for the current user
        author = Author.objects.get(user=self.request.user)
        serializer.save(author=author)


class RetrieveUpdateDestroyRecipeView(RetrieveUpdateDestroyAPIView):
    """
    GET: Anyone can view
    PUT/PATCH: Only owner or moderators can edit
    DELETE: Only owner or moderators can delete
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrModerator]
