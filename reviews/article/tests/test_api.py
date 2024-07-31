from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from article.models import CategoryArticle, Article
from django.urls import reverse
from rest_framework.test import APITestCase
import io

from article.serializers import ArticleSerializer


class ArticleAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser1')

        self.cat1 = CategoryArticle.objects.create(
            name='Test Category 1',
            slug='test-category-1'
        )
        self.cat2 = CategoryArticle.objects.create(
            name='Test Category 2',
            slug='test-category-2'
        )

        self.article_test = Article.objects.create(
            title="Test Article 1",
            content="This is not a test article.",
            slug="this-is-a-test-article-1",
            category=self.cat1
        )
        self.article_test2 = Article.objects.create(
            title="XTest Article",
            content="This is a 2 test article.",
            slug="this-is-a-test-article-2",
            category=self.cat2
        )
        self.article_test3 = Article.objects.create(
            title="XTest Article",
            content="This is a 3 test article.",
            slug="this-is-a-test-article-3",
            category=self.cat1
        )

    def test_get(self):
        url = reverse('article-list')
        response = self.client.get(url)
        serializer_data = ArticleSerializer([self.article_test, self.article_test2,
                                             self.article_test3], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('article-list')
        response = self.client.get(url, data={'category': self.cat1.pk})
        serializer_data = ArticleSerializer([self.article_test, self.article_test3], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('article-list')
        response = self.client.get(url, data={"title": "XTest Article"})
        serializer_data = ArticleSerializer([self.article_test2, self.article_test3], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_get_order(self):
        url = reverse('article-list')
        response = self.client.get(url, data={"ordering": "-id"})
        serializer_data = ArticleSerializer([self.article_test3, self.article_test2, self.article_test],
                                            many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    # <<  POST >>
    def test_post(self):
        self.assertEqual(Article.objects.all().count(), 3)
        # cat2 = CategoryArticle.objects.create(
        #     name='Test Category X',
        #     slug='test-category-X'
        # )
        data = {
            'title': 'Test Article X',
            'content': 'This is a test article X.',
            'slug': 'this-is-a-test-article-X',
            'category': self.cat1.pk
        }
        content = JSONRenderer().render(data)
        self.client.force_login(self.user)
        url = reverse('article-list')
        response = self.client.post(url, data=content, content_type='application/json')
        self.assertEqual(Article.objects.all().count(), 4)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put(self):
        print(Article.objects.get(pk=self.article_test.pk).__dict__)
        data = {
            'title': self.article_test.title,
            'content': 'test test-1',
            'slug': self.article_test.slug,
            'category': self.cat1.pk
        }
        content = JSONRenderer().render(data)
        self.client.force_login(self.user)
        url = reverse('article-detail', args=(self.article_test.pk,))
        response = self.client.put(url, data=content, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.article_test = Article.objects.get(pk=self.article_test.pk)
        self.article_test.refresh_from_db()
        #
        self.assertEqual('test test-1', self.article_test.content)
        self.assertEqual(self.cat1.pk, self.article_test.category_id)

    def test_delete(self):
        self.client.force_login(self.user)
        url = reverse('article-detail', args=(self.article_test3.pk,))
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.all().count(), 2)
