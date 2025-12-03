from django.db import models

from recipe.models import Recipe


# Create your models here.
class Cookbook(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    recipes = models.ManyToManyField(Recipe, related_name="cookbooks")

    def __str__(self):
        return f"{self.title} with recipes {self.recipes}"
