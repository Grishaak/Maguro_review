from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from article.models import CategoryArticle, Article, ArticleUserRelations, Tag
from django.urls import reverse
from rest_framework.test import APITestCase
import io

from article.serializers import ArticleSerializer


class ArticleAPITestCase(APITestCase):

    def setUp(self):
        self.user_1 = User.objects.create(username='testuser1')
        self.user_2 = User.objects.create(username='testuser2')
        self.user_3 = User.objects.create(username='testuser3',
                                          is_staff=True)

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
            category=self.cat1,
            owner=self.user_1
        )
        self.article_test2 = Article.objects.create(
            title="XTest Article",
            content="This is a 2 test article.",
            slug="this-is-a-test-article-2",
            category=self.cat2,
            owner=self.user_1
        )
        self.article_test3 = Article.objects.create(
            title="XTest Article",
            content="This is a 3 test article.",
            slug="this-is-a-test-article-3",
            category=self.cat1,
            owner=self.user_1
        )
        self.tag_1 = Tag.objects.create(
            tag_name='test_tag-1',
            slug='test-tag-1'
        )
        self.tag_2 = Tag.objects.create(
            tag_name='test_tag-2',
            slug='test-tag-2'
        )
        self.tag_3 = Tag.objects.create(
            tag_name='test_tag-3',
            slug='test-tag-3'
        )

    def test_get(self):
        url = reverse('article-list')
        response = self.client.get(url)
        articles = Article.objects.annotate(
            annotated_likes=
            Count(
                Case(
                    When(article_relations__like=True,
                         then=1))),
            rating=Avg("article_relations__rating"))
        serializer_data = ArticleSerializer(articles, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('article-list')
        response = self.client.get(url, data={'category': self.cat1.pk})
        articles = Article.objects.filter(pk__in=[
            self.article_test.pk, self.article_test3.pk]).annotate(
            annotated_likes=
            Count(
                Case(
                    When(article_relations__like=True,
                         then=1))),
            rating=Avg("article_relations__rating"))
        serializer_data = ArticleSerializer(articles, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('article-list')
        response = self.client.get(url, data={"title": "XTest Article"})
        articles = Article.objects.filter(pk__in=[
            self.article_test2.pk, self.article_test3.pk]).annotate(
            annotated_likes=
            Count(
                Case(
                    When(article_relations__like=True,
                         then=1))),
            rating=Avg("article_relations__rating"))
        serializer_data = ArticleSerializer(articles, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_get_order(self):
        url = reverse('article-list')
        response = self.client.get(url, data={"ordering": "-id"})
        articles = Article.objects.annotate(
            annotated_likes=
            Count(
                Case(
                    When(article_relations__like=True,
                         then=1))),
            rating=Avg("article_relations__rating")).order_by('-id')
        serializer_data = ArticleSerializer(articles,
                                            many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    # <<  POST >>
    def test_post_by_authorized_owner(self):
        self.assertEqual(Article.objects.all().count(), 3)
        data = {
            'title': 'Test Article X',
            'content': 'This is a test article X.',
            'slug': 'this-is-a-test-article-X',
            'category': self.cat1.pk,
            'owner': self.user_3.pk
        }
        content = JSONRenderer().render(data)
        self.client.force_login(self.user_3)
        url = reverse('article-list')
        response = self.client.post(url, data=content, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.all().count(), 4)
        self.assertEqual(Article.objects.last().owner, self.user_3)

    def test_put_by_owner(self):
        data = {
            'title': self.article_test.title,
            'content': 'test test-1',
            'slug': self.article_test.slug,
            'category': self.cat1.pk
        }
        content = JSONRenderer().render(data)
        self.client.force_login(self.user_1)
        url = reverse('article-detail', args=(self.article_test.pk,))
        response = self.client.put(url, data=content, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article_test.refresh_from_db()
        self.assertEqual('test test-1', self.article_test.content)
        self.assertEqual(self.cat1.pk, self.article_test.category_id)

    def test_delete_by_owner(self):
        self.client.force_login(self.user_1)
        url = reverse('article-detail', args=(self.article_test3.pk,))
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.all().count(), 2)

    def test_put_not_by_owner(self):
        data = {
            'title': self.article_test.title,
            'content': 'test test-1',
            'slug': self.article_test.slug,
            'category': self.cat1.pk
        }
        content = JSONRenderer().render(data)
        self.client.force_login(self.user_2)
        url = reverse('article-detail', args=(self.article_test.pk,))
        response = self.client.put(url, data=content, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual({'detail': ErrorDetail(
            string='You do not have permission to perform this action.',
            code='permission_denied')}, response.data)
        self.article_test.refresh_from_db()
        self.assertEqual("This is not a test article.", self.article_test.content)
        self.assertEqual(self.cat1.pk, self.article_test.category_id)

    def test_delete_not_by_owner(self):
        self.client.force_login(self.user_2)
        url = reverse('article-detail', args=(self.article_test3.pk,))
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual({'detail': ErrorDetail(
            string='You do not have permission to perform this action.',
            code='permission_denied')}, response.data)
        self.assertEqual(Article.objects.all().count(), 3)

    def test_put_by_owner_but_staff(self):
        data = {
            'title': self.article_test.title,
            'content': 'test test-1',
            'slug': self.article_test.slug,
            'category': self.cat1.pk
        }
        content = JSONRenderer().render(data)
        self.client.force_login(self.user_3)
        url = reverse('article-detail', args=(self.article_test.pk,))
        response = self.client.put(url, data=content, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article_test.refresh_from_db()
        self.assertEqual('test test-1', self.article_test.content)
        self.assertEqual(self.cat1.pk, self.article_test.category_id)

    def test_delete_by_owner_but_staff(self):
        self.client.force_login(self.user_3)
        url = reverse('article-detail', args=(self.article_test3.pk,))
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.all().count(), 2)

    def test_tagging(self):
        self.client.force_login(self.user_2)
        url = reverse('tag-list')
        data = {
            "tag_name": "test_tag_x",
            "slug": "test-tag-x",
        }
        content = JSONRenderer().render(data)
        response = self.client.post(url, data=content, content_type='application/json')
        tag_created = Tag.objects.get(tag_name="test_tag_x")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.article_test.tagged_by.add(tag_created, self.tag_2)

        self.assertEqual(self.article_test.tagged_by.get(tag_name="test_tag_x").slug, 'test-tag-x')
        self.assertEqual(self.article_test.tagged_by.get(tag_name='test_tag-2').slug, 'test-tag-2')


class ArticleUserRelationTestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username='testuser1')
        self.user_2 = User.objects.create(username='testuser2',
                                          is_staff=True)

        self.cat1 = CategoryArticle.objects.create(
            name='Test Category 1',
            slug='test-category-1'
        )

        self.article_test = Article.objects.create(
            title="Test Article 1",
            content="This is not a test article.",
            slug="this-is-a-test-article-1",
            category=self.cat1,
            owner=self.user_1
        )

    def test_relations(self):
        self.client.force_login(self.user_2)
        url = reverse('relation-detail', args=(self.article_test.pk,))
        data = {
            "like": True,
        }
        content = JSONRenderer().render(data)
        response = self.client.patch(url, data=content, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        relation = self.article_test.article_relations.get(user=self.user_2, article=self.article_test)
        self.assertTrue(relation.like)

        data = {
            "in_bookmarks": True,
        }
        content = JSONRenderer().render(data)
        response = self.client.patch(url, data=content, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        relation = self.article_test.article_relations.get(user=self.user_2, article=self.article_test)
        self.assertTrue(relation.in_bookmarks)

    def test_wrong_relation(self):
        self.client.force_login(self.user_1)
        url = reverse('relation-detail', args=(self.article_test.pk,))
        data = {
            "rating": 8,
        }
        content = JSONRenderer().render(data)
        response = self.client.patch(url, data=content, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # relation = self.article_test.article_relations.get(user=self.user_2, article=self.article_test)
        # self.assertTrue(relation.like)
