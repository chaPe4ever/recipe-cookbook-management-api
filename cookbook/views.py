from http import HTTPStatus

from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from cookbook.models import Cookbook
from cookbook.serializers import CookbookSerializer


# Create your views here.
class ListCreateCookbookView(GenericAPIView):
    queryset = Cookbook.objects.all()
    serializer_class = CookbookSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTPStatus.CREATED)


class RetrieveUpdateDestroyCookbookView(GenericAPIView):
    queryset = Cookbook.objects.all()
    serializer_class = CookbookSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(serializer.data)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=HTTPStatus.NO_CONTENT)
