from django.contrib.auth.models import User
from django.db import models

from cookbook.models import Cookbook
from recipe.models import Recipe


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    recipes = models.ForeignKey(to=Recipe, on_delete=models.PROTECT)
    cookbooks = models.ForeignKey(to=Cookbook, on_delete=models.PROTECT)
