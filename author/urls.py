from django.urls import path

from author.views import ListCreateAuthorView, RetrieveUpdateDestroyAuthorView

urlpatterns = [
    path("authors/", ListCreateAuthorView.as_view()),
    path("authors/<int:pk>/", RetrieveUpdateDestroyAuthorView.as_view()),
]
