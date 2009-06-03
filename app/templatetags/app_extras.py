from django import template
from app.models import Item, ItemType, Role, Performer
import os,sys

register = template.Library()

@register.inclusion_tag('app/all_categories.html')
def show_all_categories():
    all_categories = ItemType.objects.order_by('name')
    return {'all_categories': all_categories}

@register.inclusion_tag('app/select_categories.html')
def select_categories(name, default):
    all_categories = ItemType.objects.order_by('name')
    return {'all_categories': all_categories, 'name': name, 'default': default}

@register.inclusion_tag('app/item_cover.html')
def get_cover(item):
    default = '/media/covers/item_default.png'
    if item.cover is None or not item.cover.name or not os.path.exists(item.cover.path):
	return {'coverurl': default, 'item': item}
    else:
	return {'coverurl': item.cover.url, 'item': item}

@register.inclusion_tag('app/item_roles.html')
def get_item_roles(item):
    roles = Role.objects.filter(item__pk=item.pk)
    return {'roles': roles, 'item': item}

@register.inclusion_tag('app/performer_roles.html')
def get_performer_roles(performer):
    roles = Role.objects.filter(performer__pk=performer.pk)
    return {'roles': roles, 'performer': performer}

