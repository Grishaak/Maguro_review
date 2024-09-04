from django.contrib.auth.models import User
from rest_framework.settings import api_settings

from .models import Article, CategoryArticle, ArticleUserRelations, Tag, TagArticleRelation
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    # tag_name = serializers.CharField(read_only=True, )

    class Meta:
        model = Tag
        fields = ('tag_name', 'slug')


class ArticleReadersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class CategoryArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryArticle
        fields = ('id', 'name',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class ArticleSerializer(serializers.ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(read_only=True, max_digits=3,
                                      decimal_places=2)

    owner = UserSerializer(read_only=True, default='unknown')
    category_fields = CategoryArticleSerializer(source='category', read_only=True, default='unknown')
    tagged = TagSerializer(read_only=True, many=True, source='tagged_by')
    readers = ArticleReadersSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', "slug", 'category', 'category_fields',
                  'rating', 'annotated_likes', 'owner', 'tagged_by', 'tagged',
                  'readers')


class ArticleUserRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleUserRelations
        fields = ('article', 'like', 'rating', 'in_bookmarks')

# class TagArticleRelationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TagArticleRelation
#         fields = "__all__"
