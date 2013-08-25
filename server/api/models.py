from django.contrib.auth.models import User
from django.db import models


class CheckList(models.Model):
    owner = models.ForeignKey(User, related_name='owned_checklists')
    title = models.CharField(max_length=64)
