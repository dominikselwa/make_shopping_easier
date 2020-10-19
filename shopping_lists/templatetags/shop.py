from django import template

register = template.Library()


@register.filter(name='in_category')
def in_shop(products, category):
    return products.filter(category=category).count() != 0
