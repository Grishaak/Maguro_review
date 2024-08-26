from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255, blank=False, db_index=True)
    category = models.ForeignKey('CategoryArticle', on_delete=models.PROTECT,
                                 related_name='articles',
                                 verbose_name='Категория')
    owner = models.ForeignKey(User,
                              on_delete=models.SET_NULL,
                              related_name='owner_articles',
                              verbose_name='Владелец',
                              null=True,)
    readers = models.ManyToManyField(User,
                                     through='ArticleUserRelations',
                                     related_name='readers_articles')
    tagged_by = models.ManyToManyField("Tag", related_name='articles',
                                       blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        indexes = [
            models.Index(fields=['-created_at'])
        ]


class CategoryArticle(models.Model):
    name = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(unique=True, max_length=255, db_index=True, verbose_name='Слаг')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [
            models.Index(fields=['-name'])
        ]


class ArticleUserRelations(models.Model):
    RATING = (
        (1, 'Horrible'),
        (2, 'Bad'),
        (3, 'Normal'),
        (4, 'Good'),
        (5, 'Excellent'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_relations')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_relations')
    like = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(default=None, choices=RATING, null=True)
    in_bookmarks = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.article}'


class Tag(models.Model):
    tag_name = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.tag_name}'


# Нет нужды использовать Таблицу для создания отношений.
# ManyToMany сама ее создаст если не указать through.

class TagArticleRelation(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='tags_relation')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                            related_name='articles_relation')

    def __str__(self):
        return f'{self.article} - {self.tag}'
