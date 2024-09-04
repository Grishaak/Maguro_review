from django.db.models import Avg

from article.models import ArticleUserRelations


def set_rating(article):
    rating_s = (ArticleUserRelations.objects
                .filter(article=article)
                .aggregate(rating=Avg('rating'))
                .get('rating'))
    article.rating = rating_s
    article.save()
