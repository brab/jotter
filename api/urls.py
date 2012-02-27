from django.conf.urls.defaults import patterns, include, url
from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource

from jotter.api.handlers import *

jlist_item_handler = Resource(jListItemHandler)

urlpatterns = patterns('',
        url(r'^item/new', jlist_item_handler),
        url(r'^item/(?P<slug>\S+)', jlist_item_handler),
        )

