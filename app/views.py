from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from CollMan.app.models import Item, ItemType

def items(request):
    first_item_list = Item.objects.all()[:5]
    return render_to_response('app/items.html', {'items': first_item_list})

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
    return HttpResponseRedirect('/manager/items/')

def item_post(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    try:
	if len(request.POST['name']) == 0:
	    return render_to_response('app/item_edit.html', {'item': item})
	type = get_object_or_404(ItemType, name=request.POST['type'])
	item.name = request.POST['name']
	item.type = type
	item.description = request.POST['description']
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
	item = Item()
	if len(request.POST['name']) == 0:
	    return render_to_response('app/item_add.html')
	item.name = request.POST['name']
	type = get_object_or_404(ItemType, name=request.POST['type'])
	item.type = type
	item.description=request.POST['description']
    except (KeyError):
	return render_to_response('app/item_add.html')
    else:
	item.save()
	return HttpResponseRedirect(item.get_absolute_url())

def category(request, type_id):
    first_item_list = Item.objects.filter(type=type_id)[:5]
    return render_to_response('app/items.html', {'items': first_item_list})
