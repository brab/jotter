"""
API Models
"""
from slugify import slugify

from django.contrib.auth.models import User
from django.db import models

from lib import increment_slug


class Budget(models.Model):
    """
    Database model representing budgets
    """
    owner = models.ForeignKey(User, related_name='owned_budgets')
    title = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta(type):
        permissions = (
                ('view_budget', 'View Budget'),
                )


class BudgetCategory(models.Model):
    """
    BudgetCategory database model
    """
    budget = models.ForeignKey(
            Budget,
            related_name='budget_categories',
            )
    title = models.CharField(max_length=64)

    # amount in cents
    amount = models.IntegerField(default=0)

    def get_amount_dollars(self):
        """
        Return the amount in dollars
        """
        return '%.2f' % (self.amount / 100.0)

    def set_amount_dollars(self, dollars):
        """
        Set the amount in dollars
        """
        self.amount = dollars * 100.0


class CheckList(models.Model):
    """
    Database model representing check lists
    """
    owner = models.ForeignKey(User, related_name='owned_checklists')
    title = models.CharField(max_length=64)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta(type):
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
