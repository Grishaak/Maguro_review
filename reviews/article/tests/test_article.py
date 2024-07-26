from unittest import TestCase

from django.urls import reverse

from article.models import Article, CategoryArticle
from rest_framework.test import APITestCase


class ArticleTest(TestCase):

    def test_create_article(self):
        cat1 = CategoryArticle.objects.create(
            name='Test Category 1',
            slug='test-category-1'
        )
        article = Article.objects.create(
            title="Test Article",
            content="This is a test article.",
            slug="this-is-a-test-article",
            category=cat1
        )
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.content, "This is a test article.")
        self.assertEqual(article.slug, "this-is-a-test-article")
        self.assertEqual(article.category.pk, cat1.pk)

    def test_create_category(self):
        category = CategoryArticle(
            name='Test Category',
            slug='test-category'
        )

        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.slug, 'test-category')
