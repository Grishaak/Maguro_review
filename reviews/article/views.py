from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet, ModelViewSet

from article.models import Article, CategoryArticle
from article.serializers import ArticleSerializer, CategoryArticleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class ArticleList(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['category', 'title']
    search_fields = ['title', 'content', 'category__name']
    ordering_fields = ['title', 'id', 'category']
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryArticleList(ModelViewSet):
    queryset = CategoryArticle.objects.all()
    serializer_class = CategoryArticleSerializer


def login_auth(request):
    return render(request, 'login.html')
