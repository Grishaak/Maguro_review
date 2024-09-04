from django.contrib.auth.models import User
from django.db.models import When, Count, Case

from article.logic import set_rating
from article.models import Article, CategoryArticle, ArticleUserRelations, Tag
from rest_framework.test import APITestCase

from article.serializers import ArticleSerializer


class ArticleAPITestCase(APITestCase):

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
        self.tag_1 = Tag.objects.create(tag_name='Test-tag-1', slug='test-tag-1')
        self.tag_4 = Tag.objects.create(tag_name='Test-tag-4', slug='test-tag-4')
        self.tag_10 = Tag.objects.create(tag_name='Test-tag-10', slug='test-tag-10')
        self.likes_relation_1 = ArticleUserRelations.objects.create(
            user=self.user_1,
            article=self.article_test,
            like=True,
            in_bookmarks=False,
            rating=3
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
            rating=5
        )
        self.likes_relation_5 = ArticleUserRelations.objects.create(
            user=self.user_5,
            article=self.article_test,
            like=False,
            in_bookmarks=False,
        )
        self.tag_relation_1 = Article.tagged_by.through.objects.create(
            article=self.article_test,
            tag=self.tag_1
        )
        self.tag_relation_2 = Article.tagged_by.through.objects.create(
            article=self.article_test,
            tag=self.tag_4
        )
        self.tag_relation_3 = Article.tagged_by.through.objects.create(
            article=self.article_test,
            tag=self.tag_10
        )

    def test_logic_ok(self):
        set_rating(self.article_test)
        article = Article.objects.get(id=self.article_test.id)
        self.assertEqual(article.rating, 3.25)
