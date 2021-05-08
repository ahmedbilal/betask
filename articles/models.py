from django.db import models
from django.db.models.fields.related import ForeignKey


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, unique=True)
    content = models.TextField()
    tags = models.ManyToManyField("Tag", related_name="articles")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Tag(models.Model):
    parent = models.ForeignKey(
        "Tag", null=True, blank=True, on_delete=models.SET_NULL, related_name="children"
    )
    name = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name
