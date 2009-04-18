from django import forms
from app.models import Item, ItemType, CD, DVD
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
