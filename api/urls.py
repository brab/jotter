from django.conf.urls.defaults import patterns, include, url
from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource

from jotter.api.handlers import *

jlist_handler = Resource(jListHandler)
jlist_item_handler = Resource(jListItemHandler)
jlist_admins_handler = Resource(jListAdminsHandler)

urlpatterns = patterns('',
        url(r'^item/new', jlist_item_handler),
        url(r'^item/(?P<slug>[-a-z0-9_]+)', jlist_item_handler),

        url(r'^jlist/admins', jlist_admins_handler),
        url(r'^jlist/(?P<slug>[-a-z0-9_]+)/admins/(?P<email>\S+)',
            jlist_admins_handler),
        url(r'^jlist/(?P<slug>[-a-z0-9_]+)', jlist_handler),
        )

