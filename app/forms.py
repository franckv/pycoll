from django import forms
from app.models import Item, ItemType, CD, DVD, Performer, PerformerType, Person, Group, Role
from app.widgets import CalendarWidget
from django.core.urlresolvers import reverse

class ItemForm(forms.ModelForm):
    addurl = '/manager/items/add/'

    type = forms.ModelChoiceField(ItemType.objects, widget=forms.Select(attrs={'onchange': 'eval(window.location="' + addurl + '" + this.value);'}))
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
    release_date = forms.DateField(widget=CalendarWidget, required=False)
    class Meta:
	model = DVD

class PerformerForm(forms.ModelForm):
    type = forms.ModelChoiceField(PerformerType.objects, widget=forms.Select(attrs={'onchange': 'eval(window.location="/manager/performers/add/" + this.value);'}))

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
    class Meta:
	model = Role
