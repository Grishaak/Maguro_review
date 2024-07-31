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
                                 related_name='category',
                                 verbose_name='Категория')
    owner = models.ForeignKey(User,
                              on_delete=models.SET_NULL,
                              related_name='owner',
                              verbose_name='Владелец',
                              null=True)

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
