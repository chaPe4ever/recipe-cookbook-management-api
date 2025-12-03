from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from order.models import Order


class BuyerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class OrderSerializer(ModelSerializer):
    buyer = BuyerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer_text", "items", "buyer"]


class OrderCreateSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "customer_text", "items", "buyer"]
        read_only_fields = ["buyer"]
