from django.db import models

class BookMark(models.Model):
  gutendex_id = models.IntegerField(unique=True, null=True)
  title = models.CharField(max_length=500)
  summaries = models.TextField(null=True)
  cover_url = models.URLField(
    blank=True,
    null=True
  )
  authors = models.JSONField(
    default=list,
    blank=True
  )
  subjects = models.JSONField(
    default=list,
    blank=True
  )
  languages = models.JSONField(
    default=list,
    blank=True
  )
  formats = models.JSONField(
    default=dict,
    blank=True
  )
  created_at = models.DateTimeField(
    auto_now_add=True
  )
  updated_at = models.DateTimeField(
    auto_now=True
  )
  def __str__(self):
    return self.title

  

  
