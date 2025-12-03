from django.db import models


# Create your models here.
class Recipe(models.Model):
    DIFFICULTY_CHOICES = [(1, "Easy"), (2, "Intermediate"), (3, "Hard")]
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    favorite = models.BooleanField(blank=True, null=True)
