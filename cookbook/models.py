from django.db import models

from recipe.models import Recipe


# Create your models here.
class Cookbook(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    recipes = models.ManyToManyField(Recipe, related_name="cookbooks", blank=True)
    author = models.ForeignKey(
        "author.Author",
        on_delete=models.CASCADE,
        related_name="cookbooks",
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            f"{self.title} by {self.author.user.username if self.author else 'Unknown'}"
        )
