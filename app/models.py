from django.db import models

# Create your models here.

class PerformerType(models.Model):
    name = models.CharField(max_length=50, choices=(('Person', 'Person'), ('Group', 'Group')))

    def __unicode__(self):
	return self.name

class Performer(models.Model):
    type = models.ForeignKey(PerformerType)

    def __unicode__(self):
	if self.type.name == 'Person':
	    return self.person.__unicode__()
	else:
	    return self.group.__unicode__()

    @models.permalink
    def get_absolute_url(self):
	return ('app.views.performer', [str(self.pk)])


    def new(cls, performertype):
	if performertype.name == 'Person':
	    performer = Person()
	elif performertype.name == 'Group':
	    performer = Group()
	else:
	    performer = Performer()

	performer.type = performertype
	return performer

    new = classmethod(new)


class Person(Performer):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __unicode__(self):
	return '%s, %s' % (self.last_name, self.first_name)

    @models.permalink
    def get_absolute_url(self):
	return ('app.views.performer', [str(self.pk)])


class Group(Performer):
    name = models.CharField(max_length=200)
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
    type = models.ForeignKey(ItemType)
    description =  models.CharField(max_length=255, blank=True)
    release_date = models.DateField(blank=True, null=True)
    creation_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField(editable=False)
    roles = models.ManyToManyField(Performer, through='Role', blank=True, editable=False)
    cover = models.FileField(upload_to='covers', blank=True)

    @models.permalink
    def get_absolute_url(self):
	return ('app.views.item', [str(self.pk)])

    def __unicode__(self):
	return self.name

    def new(cls, itemtype):
	if itemtype.name == 'CD':
	    item = CD()
	elif itemtype.name == 'DVD':
	    item = DVD()
	else:
	    item = Item()

	item.type = itemtype
	return item

    new = classmethod(new)

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

    def get_short_description(self):
	return '%s is %s' % (self.performer.__unicode__(), self.type.__unicode__())

class CD(Item):
    def __unicode__(self):
	return self.name
    
class DVD(Item):
    def __unicode__(self):
	return self.name
