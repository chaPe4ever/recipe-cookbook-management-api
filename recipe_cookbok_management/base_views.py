"""
Base view classes that allow OPTIONS (CORS preflight) without authentication.
DRF should handle OPTIONS automatically, but if permissions block it,
this ensures OPTIONS works for CORS preflight requests.
"""
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class CORSEnabledAPIView(APIView):
    """Base APIView that allows OPTIONS without authentication for CORS preflight"""

    def get_permissions(self):
        """Allow OPTIONS (CORS preflight) without authentication"""
        if self.request.method == "OPTIONS":
            return [AllowAny()]
        return super().get_permissions()
