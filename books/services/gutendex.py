import requests

class GutendexService:

  BASE_URL = "https://gutendex.com/books/"

  def __init__(self):
    self.session = requests.Session()

  def get_books(
    self,
    page=1,
    search=None,
    language=None,
    topic=None,
  ):
    params = {
      "page": page
    }

    if search:
      params["search"] = search

    if language:
      params["language"] = language

    if topic:
      params["topic"] = topic

    response = self.session.get(
      self.BASE_URL,
      params=params,
      timeout=10
    )

    response.raise_for_status()

    return response.json()

  def get_book(self, id):
    response = self.session.get(
      f"{self.BASE_URL}{id}/",
      timeout=10
    )

    response.raise_for_status()

    return response.json()

  def format_book(self, book):
    formats = book.get("formats", {})

    authors = book.get("authors", {})

    return {
      "id": book.get("id"),
      "title": book.get("title"),

      "authors": [
        author.get("name")
        for author in authors
      ],

      "cover_url": formats.get("image/jpeg"),

      "formats": {
          "epub": formats.get("application/epub+zip"),
          "html": formats.get("text/html"),
          "text": formats.get(
              "text/plain; charset=utf-8"
          ),
      },

      "subjects": book.get("subjects", []),
      "languages": book.get("languages", []),
    }