from django.shortcuts import render
from rest_framework import generics
from rest_framework.viewsets import ViewSet, ModelViewSet

from article.models import Article, CategoryArticle
from article.serializers import ArticleSerializer, CategoryArticleSerializer


class ArticleList(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CategoryArticleList(ModelViewSet):
    queryset = CategoryArticle.objects.all()
    serializer_class = CategoryArticleSerializer
