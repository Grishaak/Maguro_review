from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from article.models import CategoryArticle, Article
from django.urls import reverse
from rest_framework.test import APITestCase
import io

from article.serializers import ArticleSerializer


class ArticleAPITestCase(APITestCase):

    # def setUp(self):
    # self.cat1 = CategoryArticle.objects.create(
    #     name='Test Category 1',
    #     slug='test-category-1'
    # )
    # self.cat2 = CategoryArticle.objects.create(
    #     name='Test Category 2',
    #     slug='test-category-2'
    # )

    def test_get(self):
        cat1 = CategoryArticle.objects.create(
            name='Test Category 1',
            slug='test-category-1'
        )
        article_test = Article.objects.create(
            title="Test Article",
            content="This is a test article.",
            slug="this-is-a-test-article",
            category=cat1
        )
        url = reverse('article-list')
        response = self.client.get(url)
        serializer_data = ArticleSerializer(article_test).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([serializer_data], response.data)

    def test_post(self):
        cat2 = CategoryArticle.objects.create(
            name='Test Category 2',
            slug='test-category-2'
        )
        data = {
            'title': 'Test Article 2',
            'content': 'This is a test article 2.',
            'slug': 'this-is-a-test-article-2',
            'category': cat2.pk
        }
        content = JSONRenderer().render(data)
        url = reverse('article-list')
        response = self.client.post(url, data=content, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
