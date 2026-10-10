from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import ChangePasswordSerializer, RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
  serializer_class = RegisterSerializer
  permission_classes = [AllowAny]
  authentication_classes = []

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)

    return Response({
      "user": UserSerializer(user).data,
      "refresh": str(refresh),
      "access": str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    try:
      RefreshToken(request.data.get("refresh")).blacklist()
    except TokenError:
      return Response(
        {"detail": "Invalid or expired refresh token."},
        status=status.HTTP_400_BAD_REQUEST
      )
    return Response(status=status.HTTP_205_RESET_CONTENT)


class MeView(generics.RetrieveUpdateAPIView):
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self):
    return self.request.user


class ChangePasswordView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    request.user.set_password(serializer.validated_data["new_password"])
    request.user.save()
    return Response({"detail": "Password updated."})
