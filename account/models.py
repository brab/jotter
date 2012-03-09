from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    access_level = models.CharField(max_length=16, default='basic',
            choices=(
                ('basic', 'Basic Access'),
                ('full', 'Full Access'),
                ))

@receiver(post_save, sender=User)
def user_profile_handler(sender, **kw):
    if kw.get('created', False):
        UserProfile.objects.create(user=kw.get('instance'))

