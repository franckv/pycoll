from django.contrib.syndication.feeds import Feed
from app.models import Item

class LatestAdds(Feed):
    title = 'Latest Additions'
    link = '/couin'
    description = 'New items added to collection'

    def items(self):
	return Item.objects.all()[:5]
