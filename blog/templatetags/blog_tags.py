from django import template
from django.db.models import Count

from .. import models as m

register = template.Library()


@register.simple_tag
def get_categories():
    return m.Category.objects.all()


@register.simple_tag
def get_tags():
    return m.Tag.objects.annotate(num_articles=Count('article')).order_by('-num_articles')


@register.simple_tag
def get_authors():
    return m.Author.objects.all()
