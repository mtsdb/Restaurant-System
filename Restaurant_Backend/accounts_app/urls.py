from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomObtainAuthToken, CurrentUserView, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("auth/login/", CustomObtainAuthToken.as_view(), name="api_token_auth"),
    path("auth/me/", CurrentUserView.as_view(), name="current_user"),
    path("", include(router.urls)),
]
