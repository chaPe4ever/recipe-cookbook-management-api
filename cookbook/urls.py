from django.urls import path

from cookbook.views import ListCreateCookbookView, RetrieveUpdateDestroyCookbookView

urlpatterns = [
    path("cookbooks/", ListCreateCookbookView.as_view()),
    path("recipes/<int:pk>/", RetrieveUpdateDestroyCookbookView.as_view()),
]
