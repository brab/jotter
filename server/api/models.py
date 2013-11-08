'''
API Models
'''
from django.contrib.auth.models import User
from django.db import models


class CheckList(models.Model):
    '''
    Database model representing check lists
    '''
    owner = models.ForeignKey(User, related_name='owned_checklists')
    title = models.CharField(max_length=64)

    class Meta:
        permissions = (
                ('view_checklist', 'View Check List'),
                )
