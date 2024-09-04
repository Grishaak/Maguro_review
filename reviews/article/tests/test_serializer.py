from datetime import datetime
from time import strftime

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase
from django.utils.timezone import now
from unicodedata import decimal

from article.models import Article, CategoryArticle, ArticleUserRelations, Tag, TagArticleRelation
from article.serializers import ArticleSerializer, CategoryArticleSerializer, TagSerializer
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
        self.tag_1 = Tag.objects.create(tag_name='Test-tag-1', slug='test-tag-1')
        self.tag_4 = Tag.objects.create(tag_name='Test-tag-4', slug='test-tag-4')
        self.tag_10 = Tag.objects.create(tag_name='Test-tag-10', slug='test-tag-10')
        ArticleUserRelations.objects.create(
            user=self.user_1,
            article=self.article_test,
            like=True,
            in_bookmarks=False,
            rating=2
        )
        ArticleUserRelations.objects.create(
            user=self.user_2,
            article=self.article_test,
            like=False,
            in_bookmarks=False,
            rating=1
        )
        user_art_relate = ArticleUserRelations.objects.create(
            user=self.user_3,
            article=self.article_test,
            like=True,
            in_bookmarks=True
        )
        print(ArticleUserRelations.objects.values('rating'))
        user_art_relate.rating = 5
        user_art_relate.save()
        user_art_relate.refresh_from_db()

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

    def test_serialize_article(self):
        tags = Tag.objects.all()
        category = CategoryArticle.objects.get(id=self.cat1.id)
        articles = Article.objects.annotate(
            annotated_likes=
            Count(
                Case(
                    When(article_relations__like=True,
                         then=1))),
        )
        data_tags = TagSerializer(tags, many=True).data
        data_category = CategoryArticleSerializer(category).data
        data_article = ArticleSerializer(articles, many=True).data
        all_ratings_valid = ArticleUserRelations.objects.filter(article=self.article_test,
                                                                rating__gt=0)
        print(all_ratings_valid)
        print(ArticleUserRelations.objects.values('rating'))

        rate_rez = sum([i.rating for i in all_ratings_valid]) / len(all_ratings_valid)
        expected_data = [
            {
                'id': self.article_test.id,

                'title': 'Test Article',
                'content': 'This is a test article.',
                # 'created_at': str(self.article_test.created_at)[0:-6].replace(' ', 'T') + 'Z',
                # 'updated_at': str(self.article_test.updated_at)[0:-6].replace(' ', 'T') + 'Z',
                'slug': 'this-is-a-test-article',
                'category': self.cat1.id,
                'category_fields': data_category,
                'rating': f"{rate_rez:.2f}",
                'annotated_likes': 2,
                'owner': {
                    "username": 'testuser1'
                },
                'tagged_by': [i.id for i in tags],
                'tagged': data_tags,
                'readers': [{'id': i.id, 'username': i.user.username}
                            for i in ArticleUserRelations.objects.all()]
            }
        ]
        print(expected_data)
        print(data_article)
        self.assertEqual(data_article, expected_data)
