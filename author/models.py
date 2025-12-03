from django.conf import settings
from django.db import models

from cookbook.models import Cookbook
from recipe.models import Recipe


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author"
    )
    recipes = models.ForeignKey(to=Recipe, on_delete=models.PROTECT)
    cookbooks = models.ForeignKey(to=Cookbook, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.user.username}'s recipes {self.recipes}"
