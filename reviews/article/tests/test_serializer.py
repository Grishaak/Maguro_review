from datetime import datetime
from time import strftime

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase
from django.utils.timezone import now
from unicodedata import decimal

from article.models import Article, CategoryArticle, ArticleUserRelations
from article.serializers import ArticleSerializer
from django.utils.dateparse import parse_datetime


class ArticleSerializerTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username='testuser1')
        self.user_2 = User.objects.create(username='testuser2')
        self.user_3 = User.objects.create(username='testuser3')
        self.user_4 = User.objects.create(username='testuser4')
        self.user_5 = User.objects.create(username='testuser5')
        self.cat1 = CategoryArticle.objects.create(
            name='Test Category 1',
            slug='test-category-1'
        )
        self.article_test = Article.objects.create(
            title="Test Article",
            content="This is a test article.",
            slug="this-is-a-test-article",
            category=self.cat1,
            owner=self.user_1
        )
        self.likes_relation_1 = ArticleUserRelations.objects.create(
            user=self.user_1,
            article=self.article_test,
            like=True,
            in_bookmarks=False,
            rating=4
        )
        self.likes_relation_2 = ArticleUserRelations.objects.create(
            user=self.user_2,
            article=self.article_test,
            like=False,
            in_bookmarks=False,
            rating=1
        )
        self.likes_relation_3 = ArticleUserRelations.objects.create(
            user=self.user_3,
            article=self.article_test,
            like=True,
            in_bookmarks=True,
            rating=4
        )
        self.likes_relation_4 = ArticleUserRelations.objects.create(
            user=self.user_4,
            article=self.article_test,
            like=True,
            in_bookmarks=True,
        )
        self.likes_relation_5 = ArticleUserRelations.objects.create(
            user=self.user_5,
            article=self.article_test,
            like=False,
            in_bookmarks=False,
        )

    def test_serialize_article(self):
        articles = Article.objects.annotate(
            annotated_likes=
            Count(
                Case(
                    When(article_relations__like=True,
                         then=1))),
            rating=Avg("article_relations__rating")
        )
        data = ArticleSerializer(articles, many=True).data
        expected_data = [
            {
                'id': self.article_test.id,
                'likes_count': 3,
                'annotated_likes': 3,
                'rating': format(9 / 3, '.2f'),
                'title': 'Test Article',
                'content': 'This is a test article.',
                'created_at': str(self.article_test.created_at)[0:-6].replace(' ', 'T') + 'Z',
                'updated_at': str(self.article_test.updated_at)[0:-6].replace(' ', 'T') + 'Z',
                'slug': 'this-is-a-test-article',
                'category': self.cat1.id,
                'owner': self.user_1.id,
                'readers': [1, 2, 3, 4, 5],
                'tagged_by': [],
            }
        ]
        print(expected_data)
        print(data)
        self.assertEqual(data, expected_data)
