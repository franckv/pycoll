from django import forms

class CalendarWidget(forms.TextInput):
    class Media:
	js = ("/media/js/calendar.js",
	    "/media/js/DateTimeShortcuts.js")

    def __init__(self, attrs={}):
	super(CalendarWidget, self).__init__(attrs={'class': 'vDateField', 'size': '10'})

