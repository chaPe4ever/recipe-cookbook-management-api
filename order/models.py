from django.db import models
from django.contrib.auth.models import User

from item.models import Item


# Create your models here.
class Order(models.Model):
    customer_text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(Item, related_name='orders')
    buyer = models.ForeignKey(to=User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.buyer.username} ordered {self.items.count()} items'