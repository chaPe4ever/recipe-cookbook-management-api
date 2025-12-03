from django.urls import path

from cookbook.views import ListCreateCookbookView, RetrieveUpdateDestroyCookbookView

urlpatterns = [
    path("", ListCreateCookbookView.as_view()),
    path("<int:pk>/", RetrieveUpdateDestroyCookbookView.as_view()),
]
