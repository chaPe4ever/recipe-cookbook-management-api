import string
import random

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
def code_generator(length=12):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


class RegistrationProfile(models.Model):
    code = models.CharField(max_length=12, default=code_generator)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s registration profile to user {self.user}"
