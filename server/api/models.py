"""
API Models
"""
from slugify import slugify

from django.contrib.auth.models import User
from django.db import models

from lib import increment_slug


class CheckList(models.Model):
    """
    Database model representing check lists
    """
    owner = models.ForeignKey(User, related_name='owned_checklists')
    title = models.CharField(max_length=64)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
                ('view_checklist', 'View Check List'),
                )

    def save(self, *args, **kw):
        """
        Override the existing method
        """
        if not self.slug:
            all_slugs = CheckList.objects \
                    .filter(owner=self.owner) \
                    .values_list('slug', flat=True)
            slug = slugify(self.title)
            while slug in all_slugs:
                slug = increment_slug(slug)
            self.slug = slug
        super(CheckList, self).save(*args, **kw)


class CheckListItem(models.Model):
    """
    Database model for check list items
    """
    check_list = models.ForeignKey(
            CheckList,
            related_name='check_list_items',
            )
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256, null=True, blank=True)
    checked = models.BooleanField(default=False)
