from blog_app.models import Category
from django import template


register = template.Library()


@register.simple_tag()
def blog_categories():
    return Category.objects.all()
