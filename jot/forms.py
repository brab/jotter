from django import forms
from django.contrib.auth.models import User

from jotter.jot.models import jList

class jListForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
            queryset=User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = jList
        exclude = ('created', 'modified', 'slug',)

