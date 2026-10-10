from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthAPITestCase(APITestCase):

  def setUp(self):
    self.password = "S3cure-pass-123"
    self.user = User.objects.create_user(username="reader", password=self.password)

  def login(self):
    response = self.client.post(
      "/api/auth/login/",
      {"username": "reader", "password": self.password}
    )
    return response.data

  def test_register(self):
    response = self.client.post("/api/auth/register/", {
      "username": "newreader",
      "email": "new@example.com",
      "password": "An0ther-pass-456",
      "password2": "An0ther-pass-456",
    })
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertIn("access", response.data)
    self.assertTrue(User.objects.filter(username="newreader").exists())

  def test_register_password_mismatch(self):
    response = self.client.post("/api/auth/register/", {
      "username": "newreader",
      "password": "An0ther-pass-456",
      "password2": "different-pass-789",
    })
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_login_and_me(self):
    tokens = self.login()
    self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    response = self.client.get("/api/auth/me/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data["username"], "reader")

  def test_me_requires_auth(self):
    response = self.client.get("/api/auth/me/")
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_logout_blacklists_refresh_token(self):
    tokens = self.login()
    self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    response = self.client.post("/api/auth/logout/", {"refresh": tokens["refresh"]})
    self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    response = self.client.post("/api/auth/token/refresh/", {"refresh": tokens["refresh"]})
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_change_password(self):
    tokens = self.login()
    self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    response = self.client.post("/api/auth/change-password/", {
      "old_password": self.password,
      "new_password": "Brand-new-pass-789",
    })
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.user.refresh_from_db()
    self.assertTrue(self.user.check_password("Brand-new-pass-789"))
