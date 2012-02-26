from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template

from jotter.jot.models import jList, jListItem

def login(request):
    redirect = request.GET.get('next', '')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password'))
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(redirect \
                        if redirect \
                        else reverse('jotter.account.views.index'))
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return direct_to_template(request, 'account/login.html', {
        'form': form,
        })

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('jotter.account.views.index'))

def index(request):
    if request.user.is_authenticated():
        user = request.user
        jlists = user.owned_jlists.all() | \
                user.admined_jlists \
                .extra(select={'is_owner':'owner_id=%s' % user.id}) \
                .all()
        jlists = jlists.order_by('name')
        if jlists.count() == 0:
            return HttpResponseRedirect(reverse(
                'jotter.jot.views.jlist_edit'))
        return direct_to_template(request, 'dashboard.html', {
            'jlists': jlists,
            })
    else:
        return direct_to_template(request, 'landing.html', {
            'form': AuthenticationForm(),
            })

