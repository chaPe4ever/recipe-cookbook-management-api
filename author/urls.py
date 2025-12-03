from django.urls import path

from author.views import ListCreateAuthorView, RetrieveUpdateDestroyAuthorView

urlpatterns = [
    path("", ListCreateAuthorView.as_view()),
    path("<int:pk>/", RetrieveUpdateDestroyAuthorView.as_view()),
]
