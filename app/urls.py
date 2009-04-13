from django.conf.urls.defaults import *

urlpatterns = patterns('app.views',
    (r'^$', 'home'),
    (r'^items/$', 'items'),
    (r'^items/(?P<item_id>\d+)/$', 'item'),
    (r'^items/(?P<item_id>\d+)/edit/$', 'item_edit'),
    (r'^items/(?P<item_id>\d+)/delete/$', 'item_delete'),
    (r'^items/(?P<item_id>\d+)/delete/force/$', 'item_delete_force'),
    (r'^items/add/$', 'item_add'),
    (r'^items/search/$', 'items_search'),
    (r'^categories/$', 'all_categories'),
    (r'^categories/(?P<type_id>\d+)/$', 'category'),
)
