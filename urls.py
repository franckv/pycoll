from django.conf.urls.defaults import *
from CollMan.settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/manager/'}),
    (r'^manager/', include('CollMan.app.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'^admin/(.*)', admin.site.root),
)
