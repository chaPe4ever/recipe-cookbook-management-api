from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from registration_profile.models import RegistrationProfile
from registration_profile.serializers import RegistrationProfileSerializer


class ListCreateRegistrationProfileView(ListCreateAPIView):
    queryset = RegistrationProfile.objects.all()
    serializer_class = RegistrationProfileSerializer
    permission_classes = [IsAuthenticated]
