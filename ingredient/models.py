from django.db import models
from django.db.models import ManyToManyField

from recipe.models import Recipe


# Create your models here.
class Ingredient(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    recipes = ManyToManyField(to=Recipe, related_name="ingredients")

    def __str__(self):
        return f"{self.title} is included in recipes {self.recipes}"
