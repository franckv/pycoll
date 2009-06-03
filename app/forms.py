from django import forms
from models import Item, ItemType, CD, DVD, Performer, PerformerType, Person, Group, Role
from widgets import CalendarWidget

class ItemForm(forms.ModelForm):
    release_date = forms.DateField(widget=CalendarWidget, required=False)
    tags = forms.CharField(required=False)

    def get_form(cls, itemtype):
	if itemtype is None:
	    formType = ItemForm
	elif itemtype.name == 'CD':
	    formType = CDForm
	elif itemtype.name == 'DVD':
	    formType = DVDForm
	else:
	    formType = ItemForm

	return formType

    get_form = classmethod(get_form)

    class Meta:
	model = Item

class CDForm(ItemForm):
    class Meta:
	model = CD

class DVDForm(ItemForm):
    description = forms.CharField(widget=forms.Textarea)
    class Meta:
	model = DVD

class PerformerForm(forms.ModelForm):
    def get_form(cls, performertype):
	if performertype is None:
	    formType = PerformerForm
	elif performertype.name == 'Person':
	    formType = PersonForm
	elif performertype.name == 'Group':
	    formType = GroupForm
	else:
	    formType = PerformerForm

	return formType


    get_form = classmethod(get_form)

    class Meta:
	model = Performer

class PersonForm(PerformerForm):
    class Meta:
	model = Person

class GroupForm(PerformerForm):
    class Meta:
	model = Group

class RoleForm(forms.ModelForm):
    item = forms.ModelChoiceField(queryset=Item.objects.all().order_by('name'))
    performer = forms.ModelChoiceField(queryset=Performer.objects.all().order_by('name'))
    class Meta:
	model = Role

class SearchForm(forms.Form):
    name = forms.CharField(required=False)
    type = forms.ModelChoiceField(ItemType.objects, required=False)

class ImportForm(forms.Form):
    file = forms.FileField()
