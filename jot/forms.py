from django import forms
from django.contrib.auth.models import User

from jotter.jot.models import jList, jListItem

class jListForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
            queryset=User.objects.all(), widget=forms.HiddenInput())
    name = forms.CharField(
            widget=forms.TextInput(attrs={'class':'span3'}))

    class Meta:
        model = jList
        exclude = ('created', 'modified', 'slug', 'admins',)

class jListItemForm(forms.ModelForm):
    jlist = forms.ModelChoiceField(
            queryset=jList.objects.all(), widget=forms.HiddenInput())
    slug = forms.CharField(
            required=False,
            widget=forms.HiddenInput())
    checked = forms.BooleanField(
            required=False,
            widget=forms.HiddenInput())
    name = forms.CharField(
            widget=forms.TextInput(attrs={'class':'span4'}))
    description = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={'class':'span4','rows':'2',}))

    class Meta:
        model = jListItem

