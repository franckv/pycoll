from django.conf.urls.defaults import *
from django.contrib import admin
from feeds import LatestAdds

feeds = {
    'adds': LatestAdds
}

urlpatterns = patterns('app.views',
    (r'^$', 'home'),
    (r'^items/$', 'items'),
    (r'^items/(?P<item_id>\d+)/$', 'item'),
    (r'^items/(?P<item_id>\d+)/edit/$', 'item_edit'),
    (r'^items/(?P<item_id>\d+)/delete/$', 'item_delete'),
    (r'^items/(?P<item_id>\d+)/delete/force/$', 'item_delete_force'),
    (r'^items/add/(?P<type_id>\d+)/$', 'item_add'),
    (r'^items/add/$', 'item_add'),
    (r'^items/search/$', 'items_search'),
    (r'^items/import/$', 'items_import'),
    (r'^categories/$', 'all_categories'),
    (r'^categories/(?P<type_id>\d+)/$', 'category'),
    (r'^performers/(?P<performer_id>\d+)/$', 'performer'),
    (r'^performers/(?P<performer_id>\d+)/edit/$', 'performer_edit'),
    (r'^performers/add/(?P<type_id>\d+)/$', 'performer_add'),
    (r'^performers/add/$', 'performer_add'),
    (r'^performers/(?P<performer_id>\d+)/delete/$', 'performer_delete'),
    (r'^performers/(?P<performer_id>\d+)/delete/force/$', 'performer_delete_force'),
    (r'^roles/(?P<role_id>\d+)/$', 'role'),
    (r'^roles/(?P<role_id>\d+)/edit/$', 'role_edit'),
    (r'^roles/add/(?P<item_id>\d+)/$', 'role_item_add'),
    (r'^roles/add/$', 'role_add'),
    (r'^roles/(?P<role_id>\d+)/delete/$', 'role_delete'),
    (r'^tags/(?P<tag_id>\d+)/$', 'tag'),
    (r'^lookup/tags/$', 'lookup_tags'),
)

urlpatterns += patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
