from rest_framework import serializers

from articles.models import Article, Tag


class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Tag.objects.all()
    )

    class Meta:
        model = Article
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
