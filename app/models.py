from django.db import models

# Create your models here.

class Performer(models.Model):
    type = models.CharField(max_length=50, choices=(('Person', 'Person'), ('Group', 'Group')))

    def __unicode__(self):
	if self.type == 'Person':
	    return self.person.__unicode__()
	else:
	    return self.group.__unicode__()

class Person(Performer):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __unicode__(self):
	return '%s, %s' % (self.last_name, self.first_name)

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
    creation_date = models.DateTimeField()
    update_date = models.DateTimeField()
    roles = models.ManyToManyField(Performer, through='Role', blank=True)

    @models.permalink
    def get_absolute_url(self):
	return ('app.views.item', [str(self.pk)])

    def __unicode__(self):
	return self.name

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

    def __unicode__(self):
	return '%s is %s of %s' % (self.performer.__unicode__(), self.type.__unicode__(), self.item.__unicode__())

class CD(Item):
    def __unicode__(self):
	return self.name
    
class DVD(Item):
    def __unicode__(self):
	return self.name
