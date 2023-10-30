import datetime

from django.db import models
from django.db.models import Count


class PostQuerySet(models.QuerySet):

    def published_post(self):
        """Фильтрует посты is_published = True и дата менее текущей."""
        return self.filter(is_published=True,
                           pub_date__lte=datetime.datetime.now())

    def published_category(self):
        """Фильтрует категорию is_published = True."""
        return self.filter(category__is_published=True)

    def count_comment(self):
        """Воззвращает количество комментариев к посту."""
        return self.annotate(comment_count=Count("comments")
                             ).order_by("-pub_date")
