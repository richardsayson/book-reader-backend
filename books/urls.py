from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BookViewSet, books, book

router = DefaultRouter()

router.register(
  "bookmark", BookViewSet, basename="bookmark"
)

urlpatterns = [
  path("books/", books),
  path("book/", book),
  path("",include(router.urls))
]