from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('jotter.jot.views',
    url(r'^(?P<slug>\S+)/edit$', 'jlist_edit'),
    url(r'^(?P<slug>\S+)/delete$', 'jlist_delete'),
    url(r'^new$', 'jlist_edit'),
    url(r'^(?P<slug>\S+)$', 'jlist_view'),
)

