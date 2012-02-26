from django.contrib.auth.models import User
from django.db import models

from jotter import slugify, increment_slug

class jList(models.Model):
    owner = models.ForeignKey(User, related_name='owned_jlists')
    admins = models.ManyToManyField(User, related_name='admined_jlists',
            null=True, blank=True)
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kw):
        try:
            jlist = jList.objects.get(id=self.id)
        except jList.DoesNotExist:
            pass

        if not self.id \
        or not jList.name == self.name:
            all_slugs = [l.slug for l in jList.objects.all()]
            slug = slugify(self.name)
            while slug in all_slugs:
                slug = increment_slug(slug)
            self.slug = slug
        super(jList, self).save(*args, **kw)

class jListItem(models.Model):
    jlist = models.ForeignKey(jList)
    name = models.CharField(max_length=32)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    checked = models.BooleanField(default=False)

    def save(self, *args, **kw):
        try:
            jlist_item = jListItem.objects.get(id=self.id)
        except jListItem.DoesNotExist:
            pass

        if not self.id \
        or not jListItem.name == self.name:
            all_slugs = [l.slug for l in jListItem.objects.all()]
            slug = slugify(self.name)
            while slug in all_slugs:
                slug = increment_slug(slug)
            self.slug = slug
        super(jListItem, self).save(*args, **kw)

