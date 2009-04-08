from django import template
from CollMan.app.models import ItemType
from CollMan.settings import CACHE_ROOT
import os

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
    filename = 'item_' + str(item.pk) + '.png'
    path = CACHE_ROOT + 'covers/' + filename
    url = '/covers/' + filename
    default = '/covers/item_default.png'
    if os.path.exists(path):
	return {'url': url}
    else:
	return {'url': default}

