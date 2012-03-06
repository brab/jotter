from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('jotter.jot.views',
    url(r'^(?P<slug>[-a-z0-9_]+)/edit$', 'jlist_edit'),
    url(r'^(?P<slug>[-a-z0-9_]+)/delete$', 'jlist_delete'),
    url(r'^new$', 'jlist_edit'),
    url(r'^(?P<slug>[-a-z0-9_]+)$', 'jlist_view'),
)

