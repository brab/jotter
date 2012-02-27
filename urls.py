from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.db import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'jotter.account.views.index'),
    url(r'^login$', 'jotter.account.views.login'),
    url(r'^logout$', 'jotter.account.views.logout'),
    url(r'^api/', include('jotter.api.urls')),
    url(r'^jot/', include('jotter.jot.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if settings.DEBUG is True:
    urlpatterns += patterns('',
        (r'^devmedia/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

