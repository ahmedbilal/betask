from functools import reduce

from rest_framework import filters, generics
from rest_framework.exceptions import ValidationError

from django.db.models import Q, query

from articles.models import Article, Tag
from articles.serializers import ArticleSerializer, TagSerializer


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["title", "created_at"]

    def get_queryset(self):
        queryset = Article.objects.all()
        title = self.request.query_params.get("title", "")
        content = self.request.query_params.get("content", "")
        tags = self.request.query_params.getlist("tags", [])

        query = Q(title__icontains=title, content__icontains=content)
        if tags:
            tags_in_db = Tag.objects.filter(Q(slug__in=tags) | Q(name__in=tags))
            tags_children = [tag.children.all() for tag in tags_in_db]
            tags_and_their_children = reduce(
                lambda acc, v: acc.union(v), tags_children + [tags_in_db]
            )
            query &= Q(tags__slug__in=tags_and_their_children.values("slug")) | Q(
                tags__name__in=tags_and_their_children.values("name")
            )
        return queryset.filter(query).distinct()


class TagDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def perform_destroy(self, instance):
        if instance.articles.all().exists():
            raise ValidationError(
                "Cannot delete Tag, as it has articles associated with it"
            )
        super().perform_destroy(instance)

    def perform_update(self, serializer):
        if (
            serializer.instance.articles.all().exists()
            and serializer.validated_data["slug"] != serializer.instance.slug
        ):
            raise ValidationError(
                {"slug": "Cannot update slug when Tag has associated articles"}
            )
        super().perform_update(serializer)


class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class TagListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
