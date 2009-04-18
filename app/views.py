import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse

from app.models import Item, ItemType, CD, DVD
from app.forms import ItemForm, CDForm, DVDForm


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

def item_delete(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render_to_response('app/item_delete.html', {'item': item})

def item_delete_force(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    return HttpResponseRedirect(reverse('app.views.items'))

def item_edit(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    itemtype = item.type
    if itemtype.name == 'CD':
	formType = CDForm
    elif itemtype.name == 'DVD':
	formType = DVDForm
    else:
	formType = ItemForm

    if request.method == 'POST':
	form = formType(request.POST)
	if form.is_valid():
	    item.name = form.cleaned_data['name']
	    item.type = form.cleaned_data['type']
	    item.description = form.cleaned_data['description']
	    item.release_date = form.cleaned_data['release_date']
	    item.update_date = datetime.datetime.now()
	    item.save()
	    return HttpResponseRedirect(item.get_absolute_url())
    else:
	form = formType(instance = item)

    return render_to_response('app/item_form.html', {'item': item, 'form': form})

def item_add(request):
    itemtype = get_object_or_404(ItemType, name='DVD')
    formType = ItemForm.get_form(itemtype)

    if request.method == 'POST':
	form = formType(request.POST)
	if form.is_valid():
	    item = Item.new(itemtype)
	    item.name = form.cleaned_data['name']
	    item.description = form.cleaned_data['description']
	    item.release_date = form.cleaned_data['release_date']
	    item.creation_date = datetime.datetime.now()
	    item.update_date = datetime.datetime.now()
	    item.save()
	    return HttpResponseRedirect(item.get_absolute_url())
    else:
	form = formType()

    return render_to_response('app/item_form.html', {'item': None, 'form': form})

def items_import(request):
    if request.method == 'POST':
	try:
	    pass
	except (KeyError):
	    return render_to_response('app/items_import.html')
	else:
	    return items(request)
    else:
	return render_to_response('app/items_import.html')

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
