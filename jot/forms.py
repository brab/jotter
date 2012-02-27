from django import forms
from django.contrib.auth.models import User

from jotter.jot.models import jList, jListItem

class jListForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
            queryset=User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = jList
        exclude = ('created', 'modified', 'slug',)

class jListItemForm(forms.ModelForm):
    jlist = forms.ModelChoiceField(
            queryset=jList.objects.all(), widget=forms.HiddenInput())
    slug = forms.CharField(
            required=False,
            widget=forms.HiddenInput())
    description = forms.CharField(
            required=False,
            widget=forms.Textarea())

    class Meta:
        model = jListItem

