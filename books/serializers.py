from rest_framework import serializers
from .models import BookMark

class BookSerializer(serializers.ModelSerializer):

  class Meta:
    model = BookMark
    fields = [
      "id",
      "gutendex_id",
      "title",
      "summaries",
      "cover_url",
      "authors",
      "subjects",
      "languages",
      "formats",
    ]