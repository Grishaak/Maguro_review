from rest_framework.settings import api_settings

from .models import Article, CategoryArticle
from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class CategoryArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryArticle
        fields = "__all__"
