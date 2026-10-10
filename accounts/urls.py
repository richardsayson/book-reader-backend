from django.urls import path
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
  TokenVerifyView,
)

from .views import ChangePasswordView, LogoutView, MeView, RegisterView

urlpatterns = [
  path("register/", RegisterView.as_view()),
  path("login/", TokenObtainPairView.as_view()),
  path("token/refresh/", TokenRefreshView.as_view()),
  path("token/verify/", TokenVerifyView.as_view()),
  path("logout/", LogoutView.as_view()),
  path("me/", MeView.as_view()),
  path("change-password/", ChangePasswordView.as_view()),
]
