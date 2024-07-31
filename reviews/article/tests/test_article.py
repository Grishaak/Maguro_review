from unittest import TestCase

from django.urls import reverse

from article.models import Article, CategoryArticle
from rest_framework.test import APITestCase


class ArticleTest(TestCase):
    def setUp(self):
        self.cat = CategoryArticle(
            name='Test Category',
            slug='test-category'
        )

        self.article_test = Article(
            title="Test Article",
            content="This is a test article.",
            slug="this-is-a-test-article",
            category=self.cat
        )

    def test_create_article(self):

        self.assertEqual(self.article_test.title, "Test Article")
        self.assertEqual(self.article_test.content, "This is a test article.")
        self.assertEqual(self.article_test.slug, "this-is-a-test-article")
        self.assertEqual(self.article_test.category.pk, self.cat.pk)

    def test_create_category(self):
        self.assertEqual(self.cat.name, 'Test Category')
        self.assertEqual(self.cat.slug, 'test-category')
