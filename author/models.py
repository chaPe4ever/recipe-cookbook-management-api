from django.conf import settings
from django.db import models


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author"
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
