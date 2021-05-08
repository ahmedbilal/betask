from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from articles.models import Article, Tag
from articles.tests.factories import ArticleFactory, TagFactory


class ArticleListCreateAPIViewTest(APITestCase):
    def test_list(self):
        article1, article2 = ArticleFactory.create_batch(2)
        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [article["id"] for article in response.data], [article1.id, article2.id]
        )

    def test_create(self):
        self.assertEqual(Article.objects.count(), 0)
        data = {
            "title": "Test Article",
            "slug": "test-article",
            "content": "Lorem ipsum",
        }
        response = self.client.post(reverse("article_list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        article = Article.objects.get(id=response.data["id"])  # newly-created
        self.assertEqual(article.slug, "test-article")

    def test_filtering(self):
        article1 = ArticleFactory.create(
            title="Dell M4700",
            slug="dell-m4700",
            content="It is a mobile workstation laptop",
        )
        article2 = ArticleFactory.create(
            title="Dell E5430", slug="dell-e5430", content="It is a business laptop"
        )
        article3 = ArticleFactory.create(
            title="OnePlus 3T", slug="oneplus-3t", content="It is android smartphone"
        )
        # Test Filtering by title
        response = self.client.get(reverse("article_list"), {"title": "dell"})
        self.assertEqual(
            [article["id"] for article in response.json()], [article1.id, article2.id]
        )

        # Test Filtering by Content
        response = self.client.get(reverse("article_list"), {"content": "laptop"})
        self.assertEqual(
            [article["id"] for article in response.json()], [article1.id, article2.id]
        )

        response = self.client.get(reverse("article_list"), {"content": "android"})
        self.assertEqual([article["id"] for article in response.json()], [article3.id])

    def test_sorting(self):
        article1 = ArticleFactory.create(
            title="Dell M4700",
            slug="dell-m4700",
            content="It is a mobile workstation laptop",
        )
        article2 = ArticleFactory.create(
            title="Dell E5430", slug="dell-e5430", content="It is a business laptop"
        )
        article3 = ArticleFactory.create(
            title="OnePlus 3T", slug="oneplus-3t", content="It is android smartphone"
        )

        # Test sorting by title
        response = self.client.get(reverse("article_list"), {"ordering": "title"})
        self.assertEqual(
            [article["id"] for article in response.json()],
            [article2.id, article1.id, article3.id],
        )

        # Test sorting by created_at
        response = self.client.get(reverse("article_list"), {"ordering": "created_at"})
        self.assertEqual(
            [article["id"] for article in response.json()],
            [article1.id, article2.id, article3.id],
        )

        # Test sorting by created_at in descending order
        response = self.client.get(reverse("article_list"), {"ordering": "-created_at"})
        self.assertEqual(
            [article["id"] for article in response.json()],
            [article3.id, article2.id, article1.id],
        )


class ArticleDetailAPIViewTest(APITestCase):
    def test_update(self):
        article = ArticleFactory(slug="my-slug")
        data = {"slug": "updated-slug"}
        url = reverse("article_detail", args=(article.id,))
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_article = Article.objects.get(id=article.id)
        self.assertEqual(updated_article.slug, "updated-slug")

    def test_delete(self):
        article = ArticleFactory()
        url = reverse("article_detail", args=(article.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)


class TagListCreateAPIViewTest(APITestCase):
    def test_list(self):
        tag1, tag2 = TagFactory.create_batch(2)
        response = self.client.get(reverse("tag_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([tag["id"] for tag in response.json()], [tag1.id, tag2.id])

    def test_create(self):
        response = self.client.post(
            reverse("tag_list"), {"name": "Tag1", "slug": "tag1"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        tag = Tag.objects.get(id=response.json()["id"])
        self.assertEqual(tag.slug, "tag1")

        response = self.client.post(
            reverse("tag_list"), {"name": "Tag2", "slug": "tag2", "parent": 1}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json()["parent"], tag.id)
