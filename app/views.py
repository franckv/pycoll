import datetime
import csv
import logging

from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from settings import MEDIA_ROOT
from models import *
from forms import *
import tagging
from tagging.models import Tag, TaggedItem

logging.basicConfig(filename='/tmp/django.log', level=logging.DEBUG)

@login_required
def home(request):
    logging.debug('home')
    return items(request)

@login_required
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

    return render_to_response('app/items.html', {'items': first_item_list}, context_instance=RequestContext(request))


@login_required
def all_categories(request):
    return items(request)

@login_required
def items_search(request):
    logging.debug('item_search')
    if request.method == 'POST':
	form = SearchForm(request.POST)
	if form.is_valid():
	    name = form.cleaned_data['name']
	    type = form.cleaned_data['type']
	    logging.debug('name=%s, type=%s' % (name,type))

	    search_results = Item.objects.filter(name__contains = name)
	    if type is not None:
		search_results = search_results.filter(type__pk = type.pk)

	    paginator = Paginator(search_results, 5)

	    try:
		page = int(request.GET.get('page', '1'))
	    except ValueError:
		page = 1

	    try:
		first_results = paginator.page(page)
	    except (EmptyPage, InvalidPage):
		first_results = paginator.page(paginator.num_pages)

	    return render_to_response('app/items_search.html', {'form': form, 'items': first_results}, context_instance=RequestContext(request))
    else:
	form = SearchForm()

    return render_to_response('app/items_search.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render_to_response('app/item_view.html', {'item': item}, context_instance=RequestContext(request))

@login_required
def item_delete(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render_to_response('app/item_delete.html', {'item': item}, context_instance=RequestContext(request))

@login_required
def item_delete_force(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    # unlink file to prevent its deletion
    item.cover = None
    item.save()
    item.delete()
    return HttpResponseRedirect(reverse('app.views.items'))

@login_required
def item_edit(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    itemtype = item.type
    formType = ItemForm.get_form(itemtype)

    if request.method == 'POST':
	form = formType(request.POST, request.FILES)
	if form.is_valid():
	    item.name = form.cleaned_data['name']
	    item.description = form.cleaned_data['description']
	    item.release_date = form.cleaned_data['release_date']
	    item.update_date = datetime.datetime.now()
	    Tag.objects.update_tags(item, form.cleaned_data['tags'])

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
	form = formType(instance = item, initial={'tags': tagging.utils.edit_string_for_tags(Tag.objects.get_for_object(item))})

    # user should not be able to change a item type so we disable it
    # disabled fields are not submitted so we also add a hidden field for the type
    form.fields['type'].queryset = ItemType.objects.filter(pk=itemtype.pk)
    form.fields['type'].widget.attrs['disabled'] = 'disabled'
    return render_to_response('app/item_form.html', {'item': item, 'form': form}, context_instance=RequestContext(request))

@login_required
def item_add(request):
    return item_type_add(request, None)

@login_required
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
	    item.save()
	    if request.FILES.has_key('cover'):
		filename = 'item_' + str(item.pk) + '.png'
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

    addurl = reverse('app.views.item_add')
    form.fields['type'].widget.attrs['onchange'] = 'eval(window.location=\'' + addurl + '\' + this.value);'
    return render_to_response('app/item_form.html', {'item': None, 'type': itemtype, 'form': form}, context_instance=RequestContext(request))

@login_required
def items_import(request):
    if request.method == 'POST':
	form = ImportForm(request.POST, request.FILES)
	if form.is_valid():
	    if request.FILES.has_key('file'):
		reader = csv.DictReader(request.FILES['file'], delimiter=';')
		for line in reader:
		    if line.has_key('type') and line.has_key('name'):
			itemtypes = ItemType.objects.filter(name=line['type'])
			if len(itemtypes) != 1:
			    continue
			itemtype = itemtypes[0]

			item = Item.new(itemtype)
			item.creation_date = datetime.datetime.now()
			item.update_date = datetime.datetime.now()
			for col in line.keys():
			    if col == 'name' or col == 'description':
				item.__setattr__(col, line[col])

			item.save()

			for col in line.keys():
			    roletypes = RoleType.objects.filter(name__iexact=col)
			    if len(roletypes) == 1:
				performers = Performer.objects.filter(name__iexact=line[col])
				if len(performers) == 0:
				    performer = Group()
				    performer.type = get_object_or_404(PerformerType, name='Group')
				    performer.name = line[col]
				    performer.save()
				else:
				    performer = performers[0]

				role = Role()
				role.item = item
				role.type = roletypes[0]
				role.performer = performer
				role.save()
				
		return HttpResponseRedirect(reverse('app.views.items'))
    else:
	form = ImportForm()

    return render_to_response('app/items_import.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def performer(request, performer_id):
    performer = get_object_or_404(Performer, pk=performer_id)
    return render_to_response('app/performer_view.html', {'performer': performer}, context_instance=RequestContext(request))

@login_required
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

    return render_to_response('app/performer_form.html', {'performer': performer, 'form': form}, context_instance=RequestContext(request))

@login_required
def performer_add(request):
    return performer_type_add(request, None)

@login_required
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
	    performer.name = form.cleaned_data['name']
	    if (performertype.name == 'Person'):
		performer.first_name = form.cleaned_data['first_name']
		performer.last_name = form.cleaned_data['last_name']
	    performer.save()
	    return HttpResponseRedirect(performer.get_absolute_url())

    else:
	form = formType(initial={'type': type_id})

    addurl = reverse('app.views.performer_add')
    form.fields['type'].widget.attrs['onchange'] = 'eval(window.location=\'' + addurl + '\' + this.value);'
    return render_to_response('app/performer_form.html', {'performer': None, 'type': performertype, 'form': form}, context_instance=RequestContext(request))

@login_required
def performer_delete(request, performer_id):
    performer = get_object_or_404(Performer, pk=performer_id)
    return render_to_response('app/performer_delete.html', {'performer': performer}, context_instance=RequestContext(request))

@login_required
def performer_delete_force(request, performer_id):
    performer = get_object_or_404(Performer, pk=performer_id)
    performer.delete()
    return HttpResponseRedirect(reverse('app.views.items'))

@login_required
def role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    return render_to_response('app/role_view.html', {'role': role}, context_instance=RequestContext(request))

@login_required
def role_edit(request, role_id):
    logging.debug('role_edit')
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

    return render_to_response('app/role_form.html', {'role': role, 'form': form}, context_instance=RequestContext(request))

@login_required
def role_add(request):
    return role_item_add(request, None)

@login_required
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

    return render_to_response('app/role_form.html', {'role': None, 'form': form}, context_instance=RequestContext(request))

@login_required
def role_delete(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    item_id = role.item.pk
    role.delete()
    return HttpResponseRedirect(reverse('app.views.item', args=[item_id]))

@login_required
def category(request, type_id):
    itemtype = get_object_or_404(ItemType, pk=type_id)
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

    return render_to_response('app/items.html', {'items': first_item_list, 'header': 'with category ' + itemtype.name}, context_instance=RequestContext(request))

@login_required
def tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    item_list = TaggedItem.objects.get_by_model(Item, tag)
    paginator = Paginator(item_list, 5)

    try:
	page = int(request.GET.get('page', '1'))
    except ValueError:
	page = 1

    try:
	first_item_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
	first_item_list = paginator.page(paginator.num_pages)

    return render_to_response('app/items.html', {'items': first_item_list, 'header': 'tagged with ' + tag.name}, context_instance=RequestContext(request))

@login_required
def lookup_tags(request):
    logging.debug('lookup_tags')
    results = ''
    if request.method == "GET":
	if request.GET.has_key(u'q'):
	    value = request.GET[u'q']
	    logging.debug(value)

	    if request.GET.has_key(u'val'):
		full = request.GET[u'val']
		logging.debug(full)
		current_tags = tagging.utils.parse_tag_input(full)
	    for tag in Tag.objects.usage_for_model(Item):
		if tag.name.startswith(value) and not tag.name in current_tags:
		    results += '%s|%s\n' % (tag.name, tag.name)
    return HttpResponse(results, mimetype='text/html')
