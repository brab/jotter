import re, json

from piston.handler import BaseHandler
from piston.utils import rc, throttle, validate

from jotter.jot.forms import jListItemForm
from jotter.jot.models import jListItem

class jListItemHandler(BaseHandler):
    model = jListItem

    def create(self, request):
        form = jListItemForm(data=request.data)
        if form.is_valid():
            jlist_item = form.save()
            resp = rc.CREATED
            resp.content = jlist_item.__dict__
            return resp.__dict__
        else:
            resp = rc.BAD_REQUEST
            resp.content = json.dumps(form.errors)
            return resp.__dict__

    def update(self, request, slug):
        try:
            item = jListItem.objects.get(slug=slug)
        except:
            resp = rc.BAD_REQUEST
            resp.content = 'jListItem not found with slug: %s' % slug
            return resp.__dict__
        form = jListItemForm(instance=item, data=request.data)
        if form.is_valid():
            jlist_item = form.save()
            resp = rc.CREATED
            resp.content = jlist_item.__dict__
            return resp.__dict__
        else:
            resp = rc.BAD_REQUEST
            resp.content = json.dumps(form.errors)
            return resp.__dict__

