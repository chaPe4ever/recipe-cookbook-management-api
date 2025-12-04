from django.db.models import Count
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from author.models import Author
from cookbook.models import Cookbook
from cookbook.serializers import CookbookSerializer
from recipe_cookbok_management.mixins import FilterMixin
from recipe_cookbok_management.permissions import IsAuthorOrReadOnly, IsOwnerOrModerator


class ListCreateCookbookView(FilterMixin, ListCreateAPIView):
    queryset = Cookbook.objects.annotate(recipe_count=Count("recipes"))
    serializer_class = CookbookSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filterset_fields = {
        "title": "title__icontains",
        "description": "description__icontains",
    }

    def perform_create(self, serializer):
        # Get the Author instance for the current user
        author = Author.objects.get(user=self.request.user)
        serializer.save(author=author)


class RetrieveUpdateDestroyCookbookView(RetrieveUpdateDestroyAPIView):
    queryset = Cookbook.objects.annotate(recipe_count=Count("recipes"))
    serializer_class = CookbookSerializer
    permission_classes = [IsOwnerOrModerator]
