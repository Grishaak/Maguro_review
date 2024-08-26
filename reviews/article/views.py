from django.db.models import When, Case, Count, Avg, expressions
from django.shortcuts import render
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet

from article.models import Article, CategoryArticle, ArticleUserRelations, Tag
from article.permissions import IsAuthenticatedAndOwnerOrReadOnlyOrStaff, \
    IsAuthenticatedAndOwnerOrReadOnlyOrStaffForTags
from article.serializers import ArticleSerializer, CategoryArticleSerializer, ArticleUserRelationSerializer, \
    TagSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins


class ArticleList(ModelViewSet):
    queryset = Article.objects.all().annotate(
        annotated_likes=
        Count(
            Case(
                When(article_relations__like=True,
                     then=1))),
        rating=Avg("article_relations__rating"))
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['category', 'title']
    search_fields = ['title', 'content', 'category__name']
    ordering_fields = ['title', 'id', 'category']
    permission_classes = [IsAuthenticatedAndOwnerOrReadOnlyOrStaff]

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class CategoryArticleList(ModelViewSet):
    queryset = CategoryArticle.objects.all()
    serializer_class = CategoryArticleSerializer


def login_auth(request):
    return render(request, 'login.html')


class ArticleUserRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ArticleUserRelations.objects.all()
    serializer_class = ArticleUserRelationSerializer
    lookup_field = 'article'

    def get_object(self):
        obj, _ = ArticleUserRelations.objects.get_or_create(user=self.request.user,
                                                            article_id=self.kwargs['article'])
        return obj


class TagView(ModelViewSet):
    permission_classes = [IsAuthenticatedAndOwnerOrReadOnlyOrStaffForTags]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
