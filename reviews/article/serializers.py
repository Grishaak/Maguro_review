from rest_framework.settings import api_settings

from .models import Article, CategoryArticle, ArticleUserRelations, Tag, TagArticleRelation
from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(read_only=True, max_digits=3,
                                      decimal_places=2)

    class Meta:
        model = Article
        fields = '__all__'

    def get_likes_count(self, instance):
        return ArticleUserRelations.objects.filter(
            article=instance,
            like=True).count()


class CategoryArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryArticle
        fields = "__all__"


class ArticleUserRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleUserRelations
        fields = ('article', 'like', 'rating', 'in_bookmarks')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

# class TagArticleRelationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TagArticleRelation
#         fields = "__all__"
