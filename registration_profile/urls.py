from django.urls import path

from registration_profile.views import ListCreateRegistrationProfileView

urlpatterns = [
    path("", ListCreateRegistrationProfileView.as_view()),
]
