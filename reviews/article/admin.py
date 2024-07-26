from django.contrib import admin
from .models import Article, CategoryArticle


class AdminArticle(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created_at', 'slug')


class AdminArticleCategory(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


admin.site.register(Article, AdminArticle)
admin.site.register(CategoryArticle, AdminArticleCategory)
