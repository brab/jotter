from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template

from jotter.jot.forms import jListForm
from jotter.jot.models import jList, jListItem

def jlist_edit(request, slug=None):
    if slug:
        try:
            jlist = jList.objects.get(slug=slug)
        except:
            messages.warning(request, 'I can\'t find that Jot')
            return HttpResponseRedirect(reverse('jotter.account.views.index'))
    else:
        jlist = None

    if request.method == 'POST':
        form = jListForm(instance=jlist, data=request.POST)
        if form.is_valid():
            jot = form.save()
            messages.success(request, 'Jot saved')
            return HttpResponseRedirect(reverse(
                'jotter.jot.views.jlist_view',
                args=[jot.slug]))
    else:
        form = jListForm(instance=jlist, initial={'owner': request.user,})
    return direct_to_template(request, 'jot/jlist_edit.html', {
        'jlist': jlist,
        'form': form,
        })

def jlist_view(request, slug):
    try:
        jlist = jList.objects.get(slug=slug)
    except:
        messages.warning(request, 'I can\'t find that Jot')
        return HttpResponseRedirect(reverse('jotter.account.views.index'))
    return direct_to_template(request, 'jot/jlist_view.html', {
        'jlist': jlist,
        })

