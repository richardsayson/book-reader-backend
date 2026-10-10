from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status


class BookAPITestCase(APITestCase):

  def test_get_books(self):
    response = self.client.get("/api/books/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_get_bookmark(self):
    response = self.client.get("/api/bookmark/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
