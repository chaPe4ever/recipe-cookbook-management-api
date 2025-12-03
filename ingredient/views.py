from http import HTTPStatus

from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ingredient.models import Ingredient
from ingredient.serializers import IngredientSerializer


# Create your views here.
class ListCreateIngredientsView(GenericAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTPStatus.CREATED)


class RetrieveUpdateDestroyIngredientView(GenericAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=HTTPStatus.NO_CONTENT)
