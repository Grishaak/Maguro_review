from datetime import datetime
from time import strftime

from django.test import TestCase
from django.utils.timezone import now

from article.models import Article, CategoryArticle
from article.serializers import ArticleSerializer
from django.utils.dateparse import parse_datetime


class ArticleSerializerTestCase(TestCase):
    def setUp(self):
        self.cat1 = CategoryArticle.objects.create(
            name='Test Category 1',
            slug='test-category-1'
        )
        self.article_test = Article.objects.create(
            title="Test Article",
            content="This is a test article.",
            slug="this-is-a-test-article",
            category=self.cat1
        )
    def test_serialize_article(self):

        data = ArticleSerializer(self.article_test).data
        expected_data = {
            'id': self.article_test.id,
            'title': 'Test Article',
            'content': 'This is a test article.',
            'created_at': str(self.article_test.created_at)[0:-6].replace(' ', 'T') + 'Z',
            'updated_at': str(self.article_test.updated_at)[0:-6].replace(' ', 'T') + 'Z',
            'slug': 'this-is-a-test-article',
            'category': self.cat1.id,
        }
        print(data)
        print(expected_data)
        self.assertEqual(expected_data, data)
