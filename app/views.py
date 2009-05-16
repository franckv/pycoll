import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse

from settings import MEDIA_ROOT

from app.models import Item, ItemType, CD, DVD, Performer, PerformerType, Person, Group, Role
from app.forms import ItemForm, CDForm, DVDForm, PerformerForm, PersonForm, GroupForm, RoleForm

import sys

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
    formType = ItemForm.get_form(itemtype)

    if request.method == 'POST':
	form = formType(request.POST, request.FILES)
	if form.is_valid():
	    item.name = form.cleaned_data['name']
	    item.type = form.cleaned_data['type']
	    item.description = form.cleaned_data['description']
	    item.release_date = form.cleaned_data['release_date']
	    item.update_date = datetime.datetime.now()
	    if request.FILES.has_key('cover'):
		filename = 'item_' + item_id + '.png'
		dest = open(MEDIA_ROOT + 'covers/' + filename, 'wb+')
		for chunk in request.FILES['cover'].chunks():
		    dest.write(chunk)
		dest.close()
		item.cover = 'covers/' + filename
	    item.save()
	    return HttpResponseRedirect(item.get_absolute_url())
    else:
	form = formType(instance = item)

    return render_to_response('app/item_form.html', {'item': item, 'form': form})

def item_add(request):
    return item_type_add(request, None)

def item_type_add(request, type_id):
    if type_id is not None:
	itemtype = get_object_or_404(ItemType, pk=type_id)
    else:
	itemtype = None

    formType = ItemForm.get_form(itemtype)

    if request.method == 'POST':
	form = formType(request.POST, request.FILES)
	if form.is_valid():
	    item = Item.new(itemtype)
	    item.name = form.cleaned_data['name']
	    item.description = form.cleaned_data['description']
	    item.release_date = form.cleaned_data['release_date']
	    item.creation_date = datetime.datetime.now()
	    item.update_date = datetime.datetime.now()
	    if request.FILES.has_key('cover'):
		filename = 'item_' + item_id + '.png'
		dest = open(MEDIA_ROOT + 'covers/' + filename, 'wb+')
		for chunk in request.FILES['cover'].chunks():
		    dest.write(chunk)
		dest.close()
		item.cover = 'covers/' + filename
	    else:
		item.cover = 'covers/item_default.png'

	    item.save()
	    return HttpResponseRedirect(item.get_absolute_url())
    else:
	form = formType(initial={'type': type_id})

    return render_to_response('app/item_form.html', {'item': None, 'type': itemtype, 'form': form})

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

def performer(request, performer_id):
    performer = get_object_or_404(Performer, pk=performer_id)
    return render_to_response('app/performer_view.html', {'performer': performer})

def performer_edit(request, performer_id):
    performer = get_object_or_404(Performer, pk=performer_id)
    performertype = performer.type
    formType = PerformerForm.get_form(performertype)

    if (performertype.name == 'Person'):
	performer = performer.person
    else:
	performer = performer.group

    if request.method == 'POST':
	form = formType(request.POST)
	if form.is_valid():
	    if (performertype.name == 'Person'):
		performer.first_name = form.cleaned_data['first_name']
		performer.last_name = form.cleaned_data['last_name']
	    else:
		performer.group.name = form.cleaned_data['name']
	    performer.save()
	    return HttpResponseRedirect(performer.get_absolute_url())
    else:
	form = formType(instance = performer)

    return render_to_response('app/performer_form.html', {'performer': performer, 'form': form})

def performer_add(request):
    return performer_type_add(request, None)

def performer_type_add(request, type_id):
    if type_id is not None:
	performertype = get_object_or_404(PerformerType, pk=type_id)
    else:
	performertype = None

    formType = PerformerForm.get_form(performertype)

    if request.method == 'POST':
	form = formType(request.POST)
	if form.is_valid():
	    performer = Performer.new(performertype)
	    if (performertype.name == 'Person'):
		performer.first_name = form.cleaned_data['first_name']
		performer.last_name = form.cleaned_data['last_name']
	    else:
		performer.name = form.cleaned_data['name']
	    performer.save()
	    return HttpResponseRedirect(performer.get_absolute_url())

    else:
	form = formType(initial={'type': type_id})

    return render_to_response('app/performer_form.html', {'performer': None, 'type': performertype, 'form': form})

def role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    return render_to_response('app/role_view.html', {'role': role})

def role_edit(request, role_id):
    role = get_object_or_404(Role, pk=role_id)

    if request.method == 'POST':
	form = RoleForm(request.POST)
	if form.is_valid():
	    role.item = form.cleaned_data['item']
	    role.type = form.cleaned_data['type']
	    role.performer = form.cleaned_data['performer']
	    role.save()
	    return HttpResponseRedirect(role.get_absolute_url())
    else:
	form = RoleForm(instance = role)

    return render_to_response('app/role_form.html', {'role': role, 'form': form})

def role_add(request):
    return role_item_add(request, None)

def role_item_add(request, item_id):
    if request.method == 'POST':
	form = RoleForm(request.POST)
	if form.is_valid():
	    role = Role()
	    role.item = form.cleaned_data['item']
	    role.type = form.cleaned_data['type']
	    role.performer = form.cleaned_data['performer']
	    role.save()
	    return HttpResponseRedirect(role.item.get_absolute_url())
    else:
	form = RoleForm(initial={'item': item_id})

    return render_to_response('app/role_form.html', {'role': None, 'form': form})

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
