import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse

from app.models import Item, ItemType, CD, DVD


def home(request):
    return items(request)

def items(request):
    item_list = Item.objects.all()
    paginator = Paginator(item_list, 5)

    try:
	page = int(request.GET.get('page', '1'))
    except ValueError:
	page = 1

    try:
	first_item_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
	first_item_list = paginator.page(paginator.num_pages)

    return render_to_response('app/items.html', {'items': first_item_list})

def all_categories(request):
    return items(request)

def items_search(request):
    pass

def item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render_to_response('app/item_view.html', {'item': item})

def item_edit(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render_to_response('app/item_edit.html', {'item': item})

def item_delete(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render_to_response('app/item_delete.html', {'item': item})

def item_delete_force(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    return HttpResponseRedirect(reverse('app.views.items'))

def item_post(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    try:
	if len(request.POST['name']) == 0:
	    return render_to_response('app/item_edit.html', {'item': item})
	type = get_object_or_404(ItemType, name=request.POST['type'])
	item.name = request.POST['name']
	item.type = type
	item.description = request.POST['description']
	item.update_date = datetime.datetime.now()
    except (KeyError):
	return render_to_response('app/item_edit.html', {'item': item})
    else:
	item.save()
	return HttpResponseRedirect(item.get_absolute_url())

def item_add(request):
    type = get_object_or_404(ItemType, name='DVD')
    return render_to_response('app/item_add.html', {'type': type})

def item_save(request):
    try:
	itemtype = get_object_or_404(ItemType, name=request.POST['type'])
	if itemtype.name == 'CD':
	    item = CD()
	    item.type = itemtype
	elif itemtype.name == 'DVD':
	    item = DVD()
	    item.type = itemtype
	else:
	    item = Item()

	if len(request.POST['name']) == 0:
	    return render_to_response('app/item_add.html')
	item.name = request.POST['name']
	item.description=request.POST['description']
	item.creation_date = datetime.datetime.now()
	item.update_date = datetime.datetime.now()
    except (KeyError):
	return render_to_response('app/item_add.html')
    else:
	item.save()
	return HttpResponseRedirect(item.get_absolute_url())

def category(request, type_id):
    item_list = Item.objects.filter(type=type_id)
    paginator = Paginator(item_list, 5)

    try:
	page = int(request.GET.get('page', '1'))
    except ValueError:
	page = 1

    try:
	first_item_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
	first_item_list = paginator.page(paginator.num_pages)

    return render_to_response('app/items.html', {'items': first_item_list})
