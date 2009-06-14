from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from tagging.fields import TagField

# Create your models here.

class PerformerType(models.Model):
    name = models.CharField(max_length=50, choices=(('Person', 'Person'), ('Group', 'Group')))

    def __unicode__(self):
	return self.name

class Performer(models.Model):
    type = models.ForeignKey(PerformerType)
    name = models.CharField(max_length=200)

    def __unicode__(self):
	if self.type.name == 'Person':
	    return self.person.__unicode__()
	elif self.type.name == 'Group': 
	    return self.group.__unicode__()
	else:
	    return self.name

    @models.permalink
    def get_absolute_url(self):
	return ('app.views.performer', [str(self.pk)])


    @classmethod
    def new(cls, performertype):
	if performertype.name == 'Person':
	    performer = Person()
	elif performertype.name == 'Group':
	    performer = Group()
	else:
	    performer = Performer()

	performer.type = performertype
	return performer

class Person(Performer):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
	displayname = ''
	if len(self.last_name) > 0:
	    displayname = self.last_name
	    if len(self.first_name) > 0:
		displayname = '%s, %s' % (displayname, self.first_name)
	else:
	    displayname = self.first_name

	#return '%s, %s' % (self.last_name, self.first_name)
	return displayname

    @models.permalink
    def get_absolute_url(self):
	return ('app.views.performer', [str(self.pk)])


class Group(Performer):
    members = models.ManyToManyField(Person)

    def __unicode__(self):
	return self.name

class ItemType(models.Model):
    name = models.CharField(max_length=50, choices=(('CD', 'CD'), ('DVD', 'DVD')))
    description = models.CharField(max_length=255)

    @models.permalink
    def get_absolute_url(self):
	return ('app.views.category', [str(self.pk)])

    def __unicode__(self):
	return self.name

class Item(models.Model):
    name =  models.CharField(max_length=255)
    alternative_name = models.CharField(max_length=255, blank=True)
    type = models.ForeignKey(ItemType)
    description =  models.CharField(max_length=255, blank=True)
    release_date = models.DateField(blank=True, null=True)
    creation_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField(editable=False)
    roles = models.ManyToManyField(Performer, through='Role', blank=True, editable=False)
    cover = models.ImageField(upload_to='covers', blank=True)

    @models.permalink
    def get_absolute_url(self):
	return ('app.views.item', [str(self.pk)])

    def __unicode__(self):
	if self.type.name == 'CD':
	    return self.cd.__unicode__()
	elif self.type.name == 'DVD':
	    return self.dvd.__unicode__()
	else:
	    return self.name

    @classmethod
    def new(cls, itemtype):
	if itemtype.name == 'CD':
	    item = CD()
	elif itemtype.name == 'DVD':
	    item = DVD()
	else:
	    item = Item()

	item.type = itemtype
	return item

    class Meta:
	ordering = ['name']

class RoleType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
	return self.name

class Role(models.Model):
    item = models.ForeignKey(Item)
    performer = models.ForeignKey(Performer)
    type = models.ForeignKey(RoleType)

    @models.permalink
    def get_absolute_url(self):
	return ('app.views.role', [str(self.pk)])

    def __unicode__(self):
	return '%s is %s of %s' % (self.performer.__unicode__(), self.type.__unicode__(), self.item.__unicode__())

class CD(Item):
    def __unicode__(self):
	try:
	    artist = Role.objects.filter(item__name = self.name).get(type__name = 'Artist').performer.name
	except:
	    artist = '?'

	return '%s - %s' % (artist, self.name)
    
class DVD(Item):
    def __unicode__(self):
	return self.name
