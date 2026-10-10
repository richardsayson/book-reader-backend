
from rest_framework import viewsets
from .models import BookMark
from .serializers import BookSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services.gutendex import GutendexService

gutendexService = GutendexService()

@api_view(["GET"])
def books(request):
  page = request.GET.get("page", 1)
  search = request.GET.get("search")
  language = request.GET.get("language")
  topic = request.GET.get("topic")

  data = gutendexService.get_books(
    page=page,
    search=search,
    language=language,
    topic=topic
  )

  results = [
    gutendexService.format_book(book)
    for book in data["results"]
  ]

  return Response({
    "count": data["count"],
    "next": data["next"],
    "previous": data["previous"],
    "results": results
  })

@api_view(["GET"])
def book(request):

  id = request.GET.get("id")

  data = gutendexService.get_book(
    id=id
  )

  results = [
    gutendexService.format_book(data)
  ]

  return Response({
    "results": results
  })

class BookViewSet(viewsets.ModelViewSet):
  queryset = BookMark.objects.all()
  serializer_class = BookSerializer
