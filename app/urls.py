from django.conf.urls.defaults import *

urlpatterns = patterns('CollMan.app.views',
    (r'^$', 'items'),
    (r'^items/$', 'items'),
    (r'^items/(?P<item_id>\d+)/$', 'item'),
    (r'^items/(?P<item_id>\d+)/edit/$', 'item_edit'),
    (r'^items/(?P<item_id>\d+)/post/$', 'item_post'),
    (r'^items/(?P<item_id>\d+)/delete/$', 'item_delete'),
    (r'^items/(?P<item_id>\d+)/delete/force/$', 'item_delete_force'),
    (r'^items/add/$', 'item_add'),
    (r'^items/save/$', 'item_save'),
    (r'^categories/(?P<type_id>\d+)/$', 'category'),
)
