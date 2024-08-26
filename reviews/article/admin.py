from django.contrib import admin
from .models import Article, CategoryArticle, ArticleUserRelations, Tag


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created_at', 'slug')


@admin.register(CategoryArticle)
class AdminArticleCategory(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


@admin.register(ArticleUserRelations)
class AdminArticleUserRelations(admin.ModelAdmin):
    list_display = ('user', 'article', 'like', 'in_bookmarks', 'rating')


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('tag_name', 'slug')
