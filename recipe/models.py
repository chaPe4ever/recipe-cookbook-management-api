from django.db import models

from author.models import Author


# Create your models here.
class Recipe(models.Model):
    DIFFICULTY_CHOICES = [(1, "Easy"), (2, "Intermediate"), (3, "Hard")]
    title = models.CharField(max_length=100)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    favorite = models.BooleanField(default=False)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="recipes",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.title} with difficulty {self.difficulty}"
