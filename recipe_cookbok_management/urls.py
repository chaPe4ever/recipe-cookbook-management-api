from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/authors/", include("author.urls")),
    path("api/cookbooks/", include("cookbook.urls")),
    path("api/ingredients/", include("ingredient.urls")),
    path("api/recipes/", include("recipe.urls")),
    path(
        "api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
    path(
        "api/token/verify/", jwt_views.TokenVerifyView.as_view(), name="token_refresh"
    ),
]
