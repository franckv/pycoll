from django import forms
from app.models import Item, ItemType, CD, DVD, Performer, PerformerType, Person, Group, Role
from app.widgets import CalendarWidget

class ItemForm(forms.ModelForm):
    def get_form(cls, itemtype):
	if itemtype.name == 'CD':
	    formType = CDForm
	elif itemtype.name == 'DVD':
	    formType = DVDForm
	else:
	    formType = ItemForm

	return formType

    get_form = classmethod(get_form)

    class Meta:
	model = Item

class CDForm(forms.ModelForm):
    class Meta:
	model = CD

class DVDForm(forms.ModelForm):
    release_date = forms.DateField(widget=CalendarWidget, required=False)
    class Meta:
	model = DVD

class PerformerForm(forms.ModelForm):
    def get_form(cls, performertype):
	if performertype.name == 'Person':
	    formType = PersonForm
	elif performertype.name == 'Group':
	    formType = GroupForm
	else:
	    formType = PerformerForm

	return formType


    get_form = classmethod(get_form)

    class Meta:
	model = Performer

class PersonForm(forms.ModelForm):
    class Meta:
	model = Person

class GroupForm(forms.ModelForm):
    class Meta:
	model = Group

class RoleForm(forms.ModelForm):
    class Meta:
	model = Role
