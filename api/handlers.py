import re, json

from django import forms
from django.contrib.auth.models import User

from piston.handler import BaseHandler
from piston.utils import rc, throttle, validate

from jotter.jot.forms import jListItemForm
from jotter.jot.models import jList, jListItem

class jListHandler(BaseHandler):
    model = jList

    def delete(self, request, slug):
        try:
            jlist = jList.objects.get(slug=slug)
        except:
            resp = rc.NOT_FOUND
            resp.content = {'error': 'jlist not found',}
            return resp.__dict__

        jlist.delete()
        resp = rc.DELETED
        return resp.__dict__


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


class jListAdminsHandler(BaseHandler):

    def create(self, request):
        email = request.data.get('email').strip()
        jlist_slug = request.data.get('jlist_slug')

        # check if it's a valid email
        f = forms.EmailField()
        try:
            f.clean(email)
        except:
            resp = rc.BAD_REQUEST
            resp.content = {'error': 'invalid email',}
            return resp.__dict__

        # is there a matching user?
        try:
            user = User.objects \
                    .exclude(id=request.user.id) \
                    .get(email__iexact=email)
        except:
            resp = rc.NOT_FOUND
            resp.content = {'error': 'user not found',}
            return resp.__dict__

        try:
            jlist = jList.objects.get(slug=jlist_slug)
        except:
            resp = rc.NOT_FOUND
            resp.content = {'error': 'jlist not found',}
            return resp.__dict__

        if user not in jlist.admins.all():
            jlist.admins.add(user)

            resp = rc.CREATED
            return resp.__dict__
        else:
            resp = rc.DUPLICATE_ENTRY
            return resp.__dict__

    def delete(self, request, slug, email):
        try:
            jlist = jList.objects.get(slug=slug)
        except:
            resp = rc.NOT_FOUND
            resp.content = {'error': 'jlist not found',}
            return resp.__dict__

        try:
            user = User.objects \
                    .exclude(id=request.user.id) \
                    .get(email__iexact=email)
        except:
            resp = rc.NOT_FOUND
            resp.content = {'error': 'user not found',}
            return resp.__dict__

        if user in jlist.admins.all():
            jlist.admins.remove(user)
            resp = rc.DELETED
            return resp.__dict__
        else:
            resp = rc.NOT_FOUND
            resp.content = {'error': 'user not admin',}
            return resp.__dict__

