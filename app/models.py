from django.db import models

# Create your models here.

class ItemType(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __unicode__(self):
	return self.name

class Item(models.Model):
    name =  models.CharField(max_length=255)
    type = models.ForeignKey(ItemType)
    description =  models.CharField(max_length=255)
    

    def __unicode__(self):
	return self.name
